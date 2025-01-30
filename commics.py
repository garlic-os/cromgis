import datetime as dt

import comics
import comics.gocomics
import dateutil.parser
from discord.ext import commands


def timedelta_normalize_timezone() -> dt.timedelta:
	"""
	Normalize datetimes instead of making them timezone-aware because the comics
	module uses timezone-naive datetimes internally
	"""
	system_now = dt.datetime.now().astimezone()
	# If for some reason your timezone's UTC offset can't be identified, just
	# default it to 0. Not that big of a deal
	system_utc_offset = dt.datetime.utcoffset(system_now) or dt.timedelta(
		hours=0
	)
	gocomics_timezone = dt.timezone(offset=dt.timedelta(hours=-5))
	gocomics_now = dt.datetime.now().astimezone(gocomics_timezone)
	gocomics_utc_offset = dt.datetime.utcoffset(gocomics_now) or dt.timedelta(
		hours=0
	)
	return gocomics_utc_offset - system_utc_offset


TIMEDELTA_NORMALIZE_TIMEZONE = timedelta_normalize_timezone()

ALIASES = {
	"calvinandhobbes": ["ch", "cnh", "calvin & hobbes", "calvin and hobbes"],
	"garfield": ["garf"],
	"heathcliff": ["hc", "heath"],
}


def get_comic_api(
	name: str, date_string: str | None
) -> comics.gocomics.ComicsAPI:
	search = comics.search(name)
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
			date = dateutil.parser.parse(date_string)
	date += TIMEDELTA_NORMALIZE_TIMEZONE
	return search.date(date)


def parse_aliases(name: str) -> str:
	name = name.lower()
	if name == "healthcliff":
		raise Exception("Heathcliff does not live healthy")
	for official_name in ALIASES:
		if name == official_name or name in ALIASES[official_name]:
			return official_name
	return name


class Comics(commands.Cog):
	"""Also made by garlicOS®"""

	@commands.command()
	async def comic(
		self, ctx: commands.Context, name: str, date: str | None = None
	) -> None:
		"""Fetch a comic by slug from GoComics.com (https://github.com/irahorecka/comics/blob/main/comics/constants/endpoints.json)"""
		name = parse_aliases(name)
		api = get_comic_api(name, date)
		await ctx.send(api.image_url)

	@commands.command(aliases=ALIASES["garfield"])
	async def garfield(
		self, ctx: commands.Context, date: str | None = None
	) -> None:
		await self.comic(ctx, "garfield", date)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Comics())
