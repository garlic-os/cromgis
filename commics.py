import comics
import datetime as dt
from discord.ext import commands

GOCOMICS_TIMEZONE = dt.timezone(offset=dt.timedelta(hours=-5))
ALIASES = {
    "calvinandhobbes": ["ch", "cnh", "calvin & hobbes"],
    "garfield": ["garf"],
}


class Comics(commands.Cog):
    """Also made by garlicOS®"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_comic_api(
        self, name: str, date: str | dt.datetime | None
    ):  # comics.ComicAPI but its not exposed in the module
        search = comics.search(name)
        if date is str:
            date = date.lower()
        match date:
            case "random" | None:
                return search.random_date()
            case "today" | "now":
                date = dt.datetime.now(tz=GOCOMICS_TIMEZONE)
            case "yesterday":
                date = dt.datetime.now(tz=GOCOMICS_TIMEZONE) - dt.timedelta(days=1)
            case "tomorrow":
                date = (
                    dt.datetime.now(tz=GOCOMICS_TIMEZONE)
                    - dt.timedelta(years=1)
                    + dt.timedelta(days=1)
                )
        return search.date(date)

    def parse_aliases(self, name: str) -> str:
        name = name.lower()
        for official_name in ALIASES:
            if name in ALIASES[official_name]:
                return official_name
        try:
            return comics.directory.search(name)[0]
        except IndexError:
            raise commands.BadArgument(f"Comic '{name}' not found")

    @commands.command()
    async def comic(
        self, ctx: commands.Context, name: str, date_string: str | None = None
    ) -> None:
        name = self.parse_aliases(name)
        api = self.get_comic_api(name, date_string)
        await ctx.send(api.get_url())

    @commands.command(aliases=ALIASES["garfield"])
    async def garfield(
        self, ctx: commands.Context, date_string: str | None = None
    ) -> None:
        await self.comic(ctx, "garfield", date_string)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Comics(bot))
