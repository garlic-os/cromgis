from typing import Any

import os
import requests
import time
import re
from discord.ext import commands

pattern_url = re.compile(r"https?:\/\/.+\.(mp4|webm)", re.IGNORECASE)


def parse_imgur_response(res: requests.Response) -> Any:
    data = res.json()["data"]
    error = data.get("error", data.get("errorCode", None))
    if error is not None:
        raise commands.BadArgument(error)
    return data


def reupload_to_imgur(video_url: str) -> str:
    params = {
        "client_id": os.environ["IMGUR_CLIENT_ID"]
    }
    payload = {
        "video": video_url,
        "type": "URL",
        "disable_audio": "1",
    }
    resp_upload = requests.post(
        "https://api.imgur.com/3/image",
        params=params, json=payload
    )
    ticket = parse_imgur_response(resp_upload)["ticket"]

    # Wait for imgur to finish processing the video
    params["tickets[]"] = ticket
    done = {}
    first_try = True
    while len(done) == 0:
        if not first_try:
            time.sleep(0.2)
        resp_album = requests.get(
            "https://imgur.com/upload/poll",
            params=params
        )
        done = parse_imgur_response(resp_album)["done"]
        first_try = False
    image_id = done[ticket]
    return f"https://i.imgur.com/{image_id}.mp4"


async def find_video_url(ctx: commands.Context) -> str:
    # Check attachments
    if len(ctx.message.attachments) != 0:
        return ctx.message.attachments[0].url
    if ctx.message.reference and ctx.message.reference.message_id:
        reference_message = await ctx.channel.fetch_message(
            ctx.message.reference.message_id
        )
        # Check reply's text
        match = pattern_url.match(reference_message.content)
        if match is not None:
            return match.group(0)
        # Check reply's attachments
        if len(reference_message.attachments) == 0:
            raise commands.BadArgument("No video provided")
        return reference_message.attachments[0].url
    raise commands.BadArgument("No video provided")


class LoopCommand(commands.Cog):
    """
    Also made by garlicOS®
    https://apidocs.imgur.com/
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def loop(self, ctx: commands.Context, *, video_url: str=None) -> None:
        """ Loop an MP4 """
        await ctx.typing()
        video_url = video_url or await find_video_url(ctx)

        # Reupload it to imgur because imgur's mp4 links magically loop
        # Also run in executor because it blocks for several seconds
        # I would have used aiohttp but it doesn't support sending its own
        # response content or TemporaryFile objects so I couldn't use it to
        # reupload a file
        link = await self.bot.loop.run_in_executor(
            None,
            reupload_to_imgur,
            video_url
        )

        await ctx.reply(link)


async def setup(bot):
    await bot.add_cog(LoopCommand(bot))
