from typing import BinaryIO

import os
from datetime import datetime, timezone
from dateutil.parser import parse as parse_date
from io import BytesIO
from dotenv import load_dotenv
from discord.ext import commands
import aiohttp
import discord

GARFIELD_URL = "https://www.gocomics.com/garfield/"


class GarfieldCommand(commands.Cog):
    """ Also made by garlicOS® """

    async def get_comic_url_by_date(self, year_month_day: str) -> str:
        """ Get the URL of a Garfield comic by date, formatted 'yyyy/mm/dd'. """
        url = GARFIELD_URL + year_month_day
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()

        # Traverse the HTML extract the comic URL within a <picture> tag
        image_tag_beg = html.find('<picture class="item-comic-image">')
        image_tag_end = html.find("</picture>", image_tag_beg)
        src_beg = html.find('src="', image_tag_beg, image_tag_end)
        src_end = html.find('"', src_beg + 5, image_tag_end)
        return html[src_beg + 5 : src_end]


    async def load_file_from_url(self, url: str) -> BytesIO:
        """ Download a file and load it into memory as a BytesIO object. """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return BytesIO(await response.read())


    @commands.command(aliases=["garf", "dailygarfield"])
    async def garfield(self, ctx: commands.Context, date: str=None) -> None:
        """
        Download a Garfield comic and post it to Discord.
        If no date given, download today's comic.
        """
        if date is not None:
            date = parse_date(date)
        else:
            date = datetime.now(timezone.utc)

        year_month_day = date.strftime("%Y/%m/%d")
        print(f"Fetching comic url for {year_month_day}...")
        comic_url = await self.get_comic_url_by_date(year_month_day)

        print("Got comic url:", comic_url)
        print("Downloading...")
        comic = await self.load_file_from_url(comic_url)

        print(f"Posting to {ctx.channel}...")
        await ctx.send(file=discord.File(
            fp=comic,
            filename=date.strftime("%Y-%m-%d") + ".gif",
        ))


def setup(bot):
    bot.add_cog(GarfieldCommand())
