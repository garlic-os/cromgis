import discord
import random
import json
import zlib
import base64
import os
from io import BytesIO
from urllib.parse import urlparse
from aiohttp import ClientSession
from discord.ext import commands
from utils import Crombed, chance, random_string
from garlic_functions import (generate_scream, generate_screech, ProbDist,
                              string_to_bf, run_bf,
                              humanize_text)

# from pyimgur import Imgur


# imgur = Imgur(os.environ["IMGUR_CLIENT_ID"])

REPLY_CHAIN_LENGTH = int(os.environ["REPLY_CHAIN_LENGTH"])


class GarlicCommands(commands.Cog):
    """ Commands made by garlicOS®! """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["aaa"])
    async def scream(self, ctx: commands.Context):
        """ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA """
        await ctx.send(generate_scream())


    @commands.command(aliases=["eee", "ree"])
    async def screech(self, ctx: commands.Context):
        """ EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE """
        await ctx.send(generate_screech())


    @commands.command(aliases=["meow", "nyan", "kitty", "kitten", "feline"])
    async def cat(self, ctx: commands.Context):
        """ Generate a cat from thiscatdoesnotexist.com. """
        url = f"https://thiscatdoesnotexist.com/?{random_string(32)}"

        embed = Crombed(
            title = "Cat"
        ).set_image(url=url)

        await ctx.reply(embed=embed)


    # This code causes an error on thispersondoesnotexist's end.
    # If you know what I can do to fix this, please tell me

    # @commands.command(aliases=["face", "facereveal", "human"])
    # async def person(self, ctx: commands.Context):
    #     """ Generate a face from thispersondoesnotexist.com. """
    #     url = f"https://thispersondoesnotexist.com/image?{random_string(32)}"

    #     # This one does not seem to play nice with Discord like the other two do,
    #     #   so it requires a little finangling to get it to work.
    #     response = requests.get(url, stream = True)

    #     img = BytesIO(response.content)

    #     embed = Crombed(
    #         title = "Person",
    #         author = ctx.author,
    #         file = discord.File(img, filename="image.jpg")
    #     )

    #     await ctx.send(embed=embed)


    @commands.command()
    async def horse(self, ctx: commands.Context):
        """ Generate a horse from thishorsedoesnotexist.com. """
        url = f"https://thishorsedoesnotexist.com/?{random_string(32)}"

        embed = Crombed(
            title = "Horse"
        ).set_image(url=url)

        await ctx.reply(embed=embed)


    @commands.command(aliases=["source", "github"])
    async def code(self, ctx: commands.Context):
        """ Look at cromgis's code! """
        embed = Crombed(
            title = "Source code",
            description = "cromgis is an open-source bot made by the /r/Ooer hivemind. See its code here:\nhttps://github.com/kaylynn234/Ooer-Discord-Bot"
        )
        await ctx.reply(embed=embed)


    @commands.command(aliases=["ev"])
    async def expectedValue(self, ctx: commands.Context, *, json_data: str):
        """ Calculate the expected value of a probability distribution. """
        try:
            probabilities = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            return await ctx.reply("Syntax error")

        prob_dist = ProbDist(probabilities)

        embed = Crombed(
            title = "Expected value",
            description = str(prob_dist.expected_value)
        )
        await ctx.reply(embed=embed)


    @commands.command(aliases=["sd"])
    async def standardDeviation(self, ctx: commands.Context, *, json_data: str):
        """ Calculate the standard deviation of a probability distribution. """
        try:
            probabilities = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            return await ctx.reply("Syntax error")

        prob_dist = ProbDist(probabilities)

        embed = Crombed(
            title = "Standard deviation",
            description = str(prob_dist.standard_deviation)
        )
        await ctx.reply(embed=embed)


    @commands.command(aliases=["bf"])
    async def executeBF(self, ctx: commands.Context, *, data: str):
        """ Execute and print the output of a BF program. """
        program_out = run_bf(data)

        embed = Crombed(
            title = "Brainfuck output",
            description = program_out
        )

        await ctx.reply(embed=embed)


    @commands.command()
    async def text2bf(self, ctx: commands.Context, *, text: str):
        """ Make a BF program that outputs the given text. """
        bf_program = string_to_bf(text)

        embed = Crombed(
            title = "Brainfuck program",
            description = bf_program
        )

        await ctx.reply(embed=embed)


    @commands.command()
    async def compress(self, ctx: commands.Context, *, data: str):
        """ Compress data with zlib (compression level 9). """
        compressed_data = zlib.compress(bytes(data, "utf-8"), 9)
        b64_text = base64.b64encode(compressed_data).decode("utf-8")

        embed = Crombed(
            title = "Compressed data",
            description = b64_text
        )

        await ctx.reply(embed=embed)


    @commands.command()
    async def decompress(self, ctx: commands.Context, *, b64_text: str):
        """ Decompress base64-encoded, zlib-compressed data. """
        decoded = base64.b64decode(b64_text)
        decompressed = zlib.decompress(decoded).decode("utf-8")

        embed = Crombed(
            title = "Decompressed data",
            description = decompressed
        )

        await ctx.reply(embed=embed)


    @commands.command(aliases=["b64e", "64e"])
    async def b64encode(self, ctx: commands.Context, *, data: str):
        """ Encode a string to base64. """
        b64_text = base64.b64encode(bytes(data, "utf-8")).decode("utf-8")

        embed = Crombed(
            title = "Base64 encoded data",
            description = b64_text
        )

        await ctx.reply(embed=embed)


    @commands.command(aliases=["b64d", "64d"])
    async def b64decode(self, ctx: commands.Context, *, b64_text: str):
        """ Decode a base64-encoded string. """
        while len(b64_text) % 4 != 0:
            b64_text += "="

        decoded_data = base64.b64decode(b64_text).decode("utf-8")

        embed = Crombed(
            title = "Base64 decoded data",
            description = decoded_data
        )

        await ctx.reply(embed=embed)


    @commands.command(aliases=["picture", "photo", "photograph"])
    @commands.cooldown(2, 4, commands.BucketType.user)
    async def image(self, ctx: commands.Context, *, raw_text: str = None):
        """
        Generate an image from text using the Text to Image API made by
        Scott Ellison Reed on deepai.org.
        """
        if raw_text:
            processed_text = humanize_text(ctx.message, raw_text)
        else:
            processed_text = random_string(32)

        print(f"[garlic.py] Fetching an ooer image based on text \"{processed_text}\"...")

        payload = {
            "text": processed_text,
        }
        headers = {
            "api-key": os.environ["DEEPAI_API_KEY"],
        }
        async with ClientSession() as session:
            async with session.post(
                "https://api.deepai.org/api/text2img",
                data=payload,
                headers=headers
            ) as response:
                response = await response.json()

            try:
                url = response["output_url"]
            except KeyError:
                raise Exception(f"Expected key 'output_url': {str(response)}")


            async with session.get(url, data=payload, headers=headers) as response:
                image = BytesIO(await response.read())


        caption = processed_text if raw_text else None  # Only show the text cromgis used if the text came from a user
        file_name = os.path.basename(urlparse(url).path)

        if os.environ.get("SPOILERIZE_AI_IMAGES", "").lower() in ("true", "1"):
            file_name = "SPOILER_" + file_name

        await ctx.reply(f"> **Image**\n> {caption}", file=discord.File(image, filename=file_name))


    # @commands.command(aliases=["mp4togif"])
    # async def mp4togifv(self, ctx: commands.Context, mp4_url: str):
    #     gifv_url = imgur.upload_image(
    #         path=mp4_url,
    #         title="cromgis video (Uploaded with PyImgur)"
    #     ).link

    #     embed = Crombed(
    #         title = "GIF converted from MP4",
    #         url = gifv_url,
    #         author = ctx.author
    #     )

    #     await ctx.send(embed=embed)


    # @commands.command()
    # async def wombo(self, ctx: commands.Context, meme_name: str, *, url: str=None):
    #     """ Lipsync a face to a meme song using wombo.ai """

    #     # Send the help message for certain words
    #     # Can't be assed to paginate the memes list right now
    #     if meme_name in ("help", "memes", "songs"):
    #         meme_names = list(wombo.MEMES.keys())
    #         with TemporaryFile() as f_memes:
    #             f_memes.writelines(meme_names)
    #             await ctx.send(
    #                 "These are the names of the memes you can use\n",
    #                 file=discord.file(f_memes, filename="wombo-memes.txt")
    #             )
    #         return

    #     # Resolve image URL
    #     if url is None and len(ctx.message.attachments) == 0:
    #         raise Exception("No image found! You must give an image URL or upload an attachment.")
    #     url = url or ctx.message.attachments[0].url

    #     # Download the image from the URL and feed it through the Wombo API
    #     async with ClientSession() as session:
    #         async with session.get(url) as response:
    #             response.raise_for_status()
    #             image = await response.read()
    #             video_url = await wombo.make_wombo(image, meme_name, session)

    #     await ctx.reply(video_url)


    # @commands.command()
    # async def garlicTest(self, ctx: commands.Context, *, text: str):
    #     embed = Crombed(
    #         title = "Test embed",
    #         description = text,
    #         author = ctx.author
    #     )

    #     await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id == message.author.id:
            # Do not respond to self
            return

        message_author_ids = set()
        message_content = set()
        async for past_message in message.channel.history(limit=REPLY_CHAIN_LENGTH):
            # Contribute to message chains
            message_author_ids.add(past_message.author.id)
            message_content.add(past_message.content)

        if len(message_content) == 1 and len(message_author_ids) >= REPLY_CHAIN_LENGTH:
            return await message.channel.send(message_content.pop())

        if chance(2 / 3):
            # Chance to say ooo 😂
            return await message.channel.send("ooo :joy:")

        # if "AAA" in message.content.upper():
        #     """ Scream in response to screams """
        #     return await message.channel.send(generate_scream())

        if "eggs benedict" in message.content.lower():
            # Say "ooo 😂" in response to "eggs benedict", per aquaa's request
            return await message.channel.send("ooo :joy:")

        if "EEE" in message.content.upper():
            # Screech in response to screeches
            return await message.channel.send(generate_screech())

        if "@someone" in message.content:
            # @someone: ping random user
            random_member = random.choice(message.guild.members)
            return await message.channel.send(random_member.mention)




def setup(bot):
    bot.add_cog(GarlicCommands(bot))
