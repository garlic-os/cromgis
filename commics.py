import datetime as dt
import random

import comics
import comics.gocomics
import dateutil.parser
from discord.ext import commands


GOCOMICS_TIMEZONE = dt.timezone(offset=dt.timedelta(hours=-5))
ALIASES = {
	"calvinandhobbes": ["ch", "cnh", "calvin & hobbes", "calvin and hobbes"],
	"garfield": ["garf"],
	"heathcliff": ["hc", "heath"],
}


class CromicsAPI(comics.gocomics.ComicsAPI):
	"""**Timezone-corrected!** user interface with GoComics."""

	def __init__(
		self, endpoint: str, title: str, date: dt.datetime | None = None
	):
		super().__init__(endpoint, title, date)
		self._date = dt.datetime(
			year=self._date.year,
			month=self._date.month,
			day=self._date.day,
			hour=12,
		).astimezone(GOCOMICS_TIMEZONE)


class Cromgisearch(comics.search):
	"""Timezone-corrected comics API search object"""

	def date(self, date: dt.datetime | str) -> CromicsAPI:
		if isinstance(date, str):
			date = dateutil.parser.parse(date)
		start_date = dt.datetime.strptime(self.start_date, "%Y-%m-%d")
		if date < start_date:
			raise comics.InvalidDateError(
				f"Search for dates after {self.start_date}. "
				f"Your input: {date.strftime('%Y-%m-%d')}"
			)
		return CromicsAPI(self.endpoint, self.title, date)

	def random_date(self) -> CromicsAPI:
		return CromicsAPI(self.endpoint, self.title)


def get_comic_api(name: str, date_string: str | None) -> CromicsAPI:
	search = Cromgisearch(name)
	match date_string:
		case "random" | None:
			return search.random_date()
		case "today" | "now":
			date = dt.datetime.now()
		case "yesterday":
			date = dt.datetime.now() - dt.timedelta(days=1)
		case "tomorrow":
			now = dt.datetime.now()
			date = dt.datetime(
				year=now.year - 1, month=now.month, day=now.day
			) - dt.timedelta(days=1)
		case _:
			date = date_string
	return search.date(date)


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

	@commands.command(aliases=["comics"])
	async def comic(
		self,
		ctx: commands.Context,
		name: str | None,
		*,
		date: str | None = None,
	) -> None:
		"""Fetch a comic by slug from GoComics.com (https://github.com/irahorecka/comics/blob/main/comics/constants/endpoints.json)"""
		say_name = name is None

		if name == "search":
			name = date
			await ctx.reply(str(comics.directory.search(name)))
			return

		name = parse_aliases(name)
		api = get_comic_api(name, date)
		content = name + "\n" if say_name else ""
		await ctx.reply(content + api.image_url)

	@commands.command(aliases=ALIASES["garfield"])
	async def garfield(
		self, ctx: commands.Context, *, date: str | None = None
	) -> None:
		await self.comic(ctx, "garfield", date=date)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Comics())
