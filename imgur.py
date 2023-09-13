
import os
import requests
from discord.ext import commands


def reupload_to_imgur(video_url: str) -> str:
    resp_video = requests.get(video_url)
    files = {
        "disable_audio": "1",
        "video": resp_video.content
    }
    params = {
        "client_id": os.environ["IMGUR_CLIENT_ID"]
    }
    resp_upload = requests.post("https://api.imgur.com/3/image", params=params, files=files)
    ticket = resp_upload.json()["data"]["ticket"]

    # idk what this part is this is just the way the imgur api works
    params["tickets[]"] = ticket
    resp_album = requests.get("https://imgur.com/upload/poll", params=params)
    image_id = resp_album.json()["data"]["done"][ticket]
    return f"https://i.imgur.com/{image_id}.mp4"


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

        # Reupload it to imgur because imgur's mp4 links magically loop
        # Run in executor because it's a blocking function
        # I would have used aiohttp but it doesn't support sending its own
        # response content or TemporaryFile objects
        link = await self.bot.loop.run_in_executor(
            None,
            reupload_to_imgur,
            video_url
        )

        await ctx.reply(link)


async def setup(bot):
    await bot.add_cog(LoopCommand(bot))
