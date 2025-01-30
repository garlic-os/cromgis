import datetime as dt

import comics
import comics.gocomics
from discord.ext import commands


GOCOMICS_TIMEZONE = dt.timezone(offset=dt.timedelta(hours=-5))
ALIASES = {
	"calvinandhobbes": ["ch", "cnh", "calvin & hobbes", "calvin and hobbes"],
	"garfield": ["garf"],
	"healthcliff": ["hc", "heath"],
}


class Comics(commands.Cog):
	"""Also made by garlicOS®"""

	@staticmethod
	def get_comic_api(
		name: str, date: str | None | dt.date | dt.datetime
	) -> comics.gocomics.ComicsAPI:
		search = comics.search(name)
		if date is not None:
			date = date or date.lower()
		match date:
			case "random" | None:
				return search.random_date()
			case "today" | "now":
				date = dt.datetime.now(tz=GOCOMICS_TIMEZONE)
			case "yesterday":
				date = dt.datetime.now(tz=GOCOMICS_TIMEZONE) - dt.timedelta(
					days=1
				)
			case "tomorrow":
				now = dt.datetime.now(tz=GOCOMICS_TIMEZONE)
				date = dt.date(
					year=now.year - 1, month=now.month, day=now.day - 1
				)
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
