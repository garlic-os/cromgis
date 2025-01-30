import datetime as dt

import comics
import comics.gocomics
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
	return system_utc_offset - gocomics_utc_offset


TIMEDELTA_NORMALIZE_TIMEZONE = timedelta_normalize_timezone()

ALIASES = {
	"calvinandhobbes": ["ch", "cnh", "calvin & hobbes", "calvin and hobbes"],
	"garfield": ["garf"],
	"healthcliff": ["hc", "heath"],
}


class Comics(commands.Cog):
	"""Also made by garlicOS®"""

	@staticmethod
	def parse_date_string(
		date_string: str | None,
	) -> dt.datetime | dt.date | None:
		if date_string is not None:
			date_string = date_string.lower()
		match date_string:
			case "today" | "now":
				date = dt.datetime.now()
			case "yesterday":
				date = dt.datetime.now() - dt.timedelta(days=1)
			case "tomorrow":
				now = dt.datetime.now()
				date = dt.date(
					year=now.year - 1, month=now.month, day=now.day - 1
				)
			case _:
				return None
		return date + TIMEDELTA_NORMALIZE_TIMEZONE

	@staticmethod
	def get_comic_api(
		name: str, date_string: str | None
	) -> comics.gocomics.ComicsAPI:
		search = comics.search(name)
		date = Comics.parse_date_string(date_string)
		if date is None:
			return search.random_date()
		return search.date(date)

	@staticmethod
	def parse_aliases(name: str) -> str:
		name = name.lower()
		for official_name in ALIASES:
			if name == official_name or name in ALIASES[official_name]:
				return official_name
		try:
			return comics.directory.search(name)[0]
		except IndexError:
			raise commands.BadArgument(f"Comic '{name}' not found")

	@commands.command()
	async def comic(
		self, ctx: commands.Context, name: str, date: str | None = None
	) -> None:
		name = Comics.parse_aliases(name)
		api = Comics.get_comic_api(name, date)
		await ctx.send(api.image_url)

	@commands.command(aliases=ALIASES["garfield"])
	async def garfield(
		self, ctx: commands.Context, date: str | None = None
	) -> None:
		await self.comic(ctx, "garfield", date)


async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Comics())
