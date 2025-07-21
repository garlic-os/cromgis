import datetime as dt
import random
from typing import TypedDict

import comics
from comics._gocomics import ComicsAPI
from discord.ext import commands


GOCOMICS_TIMEZONE = dt.timezone(offset=dt.timedelta(hours=-5))
ALIASES = {
	"calvinandhobbes": ["ch", "cnh", "calvin & hobbes", "calvin and hobbes"],
	"garfield": ["garf"],
	"heathcliff": ["hc", "heath"],
}
RETRY_COUNT = 20


class RegisteredComic(TypedDict):
	title: str
	start_date: str


type RegisteredComics = dict[str, RegisteredComic]


class TZAComicsAPI(ComicsAPI):
	"""**Timezone-aware!** user interface with GoComics."""

	def __init__(self, comics_api: ComicsAPI | comics.search):
		# bc of comics's screwed up __new__ method
		assert not isinstance(comics_api, comics.search)

		self.endpoint = comics_api.endpoint
		self.title = comics_api.title
		self._date = (
			dt.datetime(
				year=comics_api._date.year,
				month=comics_api._date.month,
				day=comics_api._date.day,
				hour=12,
			)
			.astimezone(GOCOMICS_TIMEZONE)
			.date()
		)


def get_comic_api(name: str, date_string: str | None) -> TZAComicsAPI:
	if date_string is not None:
		date_string = date_string.lower()
	match date_string:
		case "random" | "aleatoreo" | None:
			return TZAComicsAPI(comics.search(name, date="random"))
		case "today" | "now" | "ahora" | "ya" | "hoy":
			date = dt.datetime.now()
		case "yesterday" | "ayer":
			date = dt.datetime.now() - dt.timedelta(days=1)
		case "tomorrow" | "manana" | "mañana":
			now = dt.datetime.now()
			date = dt.datetime(
				year=now.year - 1, month=now.month, day=now.day
			) - dt.timedelta(days=1)
		case _:
			date = date_string
	return TZAComicsAPI(comics.search(name, date))


def parse_aliases(name: str | None) -> str:
	if name is None:
		return random.choice(comics.directory.listall())
	name = name.lower()
	if name == "healthcliff":
		raise Exception("Heathcliff does not live healthy")
	for official_name in ALIASES:
		if name == official_name or name in ALIASES[official_name]:
			return official_name
	return name


class Comics(commands.Cog):
	"""Also made by garlicOS®"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot
		# remove all hypens from the comic names. some of them have them between
		# words and some of them dont
		# copying to avoid a "dictionary changed size during iteration"
		for name in list(comics.directory._registered_comics.keys()):
			if "-" in name:
				new_name = name.replace("-", "")
				comics.directory._registered_comics[new_name] = (
					comics.directory._registered_comics.pop(name)
				)

	@commands.command(aliases=["comics"])
	async def comic(
		self,
		ctx: commands.Context,
		name: str | None,
		*,
		date: str | None = None,
	) -> None:
		"""
		Fetch a comic by slug from GoComics.com
		https://github.com/irahorecka/comics/blob/main/comics/constants/endpoints.json
		"""
		say_name = name is None
		say_date = date is None

		if name == "search":
			name = date
			await ctx.reply(str(comics.directory.search(name)))
			return

		name = parse_aliases(name)
		api = await self.stubbornly_get_comic_api(name, date)
		content = ""
		if say_name:
			content += name + "\n"
		if say_date:
			content += api.date + "\n"
		# type: ignore -- package is badly annotated; api.image_url is str
		await ctx.reply(content + api.image_url)  # type: ignore

	@commands.command(aliases=ALIASES["garfield"])
	async def garfield(
		self, ctx: commands.Context, *, date: str | None = None
	) -> None:
		await self.comic(ctx, "garfield", date=date)

	async def stubbornly_get_comic_api(
		self,
		name: str,
		date: str | None,
	) -> TZAComicsAPI:  # type: ignore -- always returns the right type or raises
		for i in range(RETRY_COUNT):
			try:
				# Run in executor because this can take like a minute now
				api = await self.bot.loop.run_in_executor(
					None, get_comic_api, name, date
				)
				api.image_url  # accessing raises if the search failed
				return api
			except comics.exceptions.InvalidDateError:
				if i == RETRY_COUNT - 1:
					raise


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Comics(bot))
