import discord
import random
import json
import zlib
import base64
import os
from urllib.parse import urlparse
from discord.ext import commands
from aiohttp import ClientSession
from io import BytesIO
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
        self.craiyon_failure_embed = Crombed(
            title="Craiyon instance expired",\
            description="cromgis needs a new Craiyon link.\n"
            "[Follow the instructions on this webpage](https://colab.research.google.com/drive/1uGpVB4GngBdONlHebVJ5maVFZDV-gtIe)"
            " to get one, then do `ooer relink <new_link>` to restore `ooer craiyon`.",
        )


    @commands.command(aliases=["aaa"])
    async def scream(self, ctx):
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
            description = "cromgis is an open-source bot made by the /r/Ooer hivemind. See its code here:\nhttps://github.com/the-garlic-os/cromgis"
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
        async with self.bot.http_session.post(
            "https://api.deepai.org/api/text2img",
            data=payload,
            headers=headers
        ) as response:
            response = await response.json()

        try:
            url = response["output_url"]
        except KeyError:
            raise Exception(f"Expected key 'output_url': {str(response)}")


        async with self.bot.http_session.get(url, data=payload, headers=headers) as response:
            image = BytesIO(await response.read())


        caption = processed_text if raw_text else None  # Only show the text cromgis used if the text came from a user
        file_name = os.path.basename(urlparse(url).path)

        if os.environ.get("SPOILERIZE_AI_IMAGES", "").lower() in ("true", "1"):
            file_name = "SPOILER_" + file_name

        await ctx.reply(f"> **Image**\n> {caption}", file=discord.File(image, filename=file_name))


    @commands.command(aliases=["dalle", "crayon"])
    @commands.cooldown(2, 4, commands.BucketType.user)
    async def craiyon(self, ctx: commands.Context, *, raw_text: str = None):
        """
        Generate an image from a self-hosted Craiyon instance. (Formerly known
        as Dall⋅E Mini)
        """
        if not hasattr(self.bot, "craiyon_url") or self.bot.craiyon_url is None:
            return await ctx.reply(embed=self.craiyon_failure_embed)

        if raw_text:
            processed_text = humanize_text(ctx.message, raw_text)
        else:
            processed_text = random_string(32)

        print(f"[garlic.py] Fetching an ooer craiyon based on text \"{processed_text}\"...")

        payload = {
            "text": processed_text,
            "num_images": 1,
        }
        async with ClientSession() as session:
            async with session.post(f"{self.bot.craiyon_url}/dalle", json=payload) as response:
                # Get response[0] without JSON parsing by just removing the
                # surrounding brackets and quotes
                data_uri = (await response.text())[2:-2]

        if len(data_uri) < 500:
            return await ctx.reply(embed=self.craiyon_failure_embed)

        # Parse response:
        # response comes as a PNG data URI;
        # we need it as a file-like object.
        image = BytesIO(base64.b64decode(data_uri))

        # Only show the text cromgis used if the text came from a user
        caption = processed_text if raw_text else None

        if os.environ.get("SPOILERIZE_AI_IMAGES", "").lower() in ("true", "1"):
            file_name = "SPOILER_craiyon.jpg"
        else:
            file_name = "craiyon.jpg"

        await ctx.reply(
            f"> **Craiyon Image**\n> {caption}",
            file=discord.File(image, filename=file_name)
        )


    @commands.command()
    @commands.cooldown(2, 4, commands.BucketType.user)
    async def relink(self, ctx: commands.Context, url: str):
        """
        Set a new Craiyon instance URL.
        """
        self.bot.craiyon_url = url
        await ctx.reply("Craiyon instance URL set. `ooer craiyon` is available once more")


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

        if "eggs benedict" in message.content.upper():
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
