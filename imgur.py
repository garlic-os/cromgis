from typing import IO

import os
from discord.ext import commands
from tempfile import TemporaryFile


class LoopCommand(commands.Cog):
    """
    Also made by garlicOS®
    https://apidocs.imgur.com/
    """

    def __init__(self, bot):
        self.bot = bot

    async def download_temp(self, url: str) -> IO:
        async with self.bot.http_session.get(url) as response:
            with TemporaryFile("w+", encoding="utf-8") as f:
                f.write(await response.text())
                f.seek(0)
                return f

    @commands.command()
    async def loop(self, ctx: commands.Context, *, video_url: str=None) -> None:
        """ Loop an MP4 """
        if video_url is None:
            # Check reply for MP4
            if ctx.message.reference and ctx.message.reference.message_id:
                reference_message = await ctx.channel.fetch_message(
                    ctx.message.reference.message_id
                )
                if len(reference_message.attachments) == 0:
                    raise commands.BadArgument("No video provided")
                video_url = ctx.message.reference.attachments[0].url
            raise commands.BadArgument("No video provided")

        # Download the video
        f = self.download_temp(video_url)

        # Reupload it to imgur because imgur's mp4 links magically loop
        url = "https://api.imgur.com/3/image"
        payload = {
            "disable_audio": 1,
            "video": f
        }
        headers = {
            "Authorization": f'Client-ID {os.environ["IMGUR_CLIENT_ID"]}'
        }
        async with self.bot.http_session.post(url, headers=headers, data=payload) as response:
            response.raise_for_status()
            data = await response.json()
            await ctx.reply(data["data"]["link"])


async def setup(bot):
    await bot.add_cog(LoopCommand(bot))
