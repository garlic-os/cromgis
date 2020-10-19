from discord.ext import commands
from utils import Crombed, chance, is_mention, extract_id, random_string
from garlic_functions import (generate_scream, generate_screech, ProbDist,
                              string_to_bf, run_bf, ooojoy, generate_gibberish)
import usernumber
import random
import json
import zlib
import base64
import requests
import os
from pyimgur import Imgur

imgur = Imgur(os.environ["IMGUR_CLIENT_ID"])

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
            title = "Cat",
            author = ctx.author
        ).set_image(url=url)
        
        await ctx.send(embed=embed)


    """ This code causes an error on thispersondoesnotexist's end.
        If you know what I can do to fix this, please tell me """
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
        """ Generate a horse from thishorsedoesnotexist.com/.com. """
        url = f"https://thishorsedoesnotexist.com/?{random_string(32)}"

        embed = Crombed(
            title = "Horse",
            author = ctx.author
        ).set_image(url=url)
        
        await ctx.send(embed=embed)


    @commands.command(aliases=["source", "github"])
    async def code(self, ctx: commands.Context):
        """ Look at cromgis's code! """
        embed = Crombed(
            title = "Source code",
            description = "cromgis is an open-source bot made by the /r/Ooer hivemind. See its code here:\nhttps://github.com/kaylynn234/Ooer-Discord-Bot"
        )
        await ctx.send(embed=embed)

    
    @commands.command(aliases=["ev"])
    async def expectedValue(self, ctx: commands.Context, *, json_data: str):
        """ Calculate the expected value of a probability distribution. """
        try:
            probabilities = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            return await ctx.send("Syntax error")

        prob_dist = ProbDist(probabilities)

        embed = Crombed(
            title = "Expected value",
            description = str(prob_dist.expected_value)
        )
        await ctx.send(embed=embed)


    @commands.command(aliases=["sd"])
    async def standardDeviation(self, ctx: commands.Context, *, json_data: str):
        """ Calculate the standard deviation of a probability distribution. """
        try:
            probabilities = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            return await ctx.send("Syntax error")

        prob_dist = ProbDist(probabilities)

        embed = Crombed(
            title = "Standard deviation",
            description = str(prob_dist.standard_deviation)
        )
        await ctx.send(embed=embed)

    
    @commands.command(aliases=["bf"])
    async def executeBF(self, ctx: commands.Context, *, data: str):
        """ Execute and print the output of a BF program. """
        program_out = run_bf

        embed = Crombed(
            title = "Brainfuck output",
            description = program_out
        )

        await ctx.send(embed=embed)

    
    @commands.command()
    async def text2bf(self, ctx: commands.Context, *, text: str):
        """ Make a BF program that outputs the given text. """
        bf_program = string_to_bf(text)

        embed = Crombed(
            title = "Brainfuck program",
            description = bf_program
        )

        await ctx.send(embed=embed)

    
    @commands.command()
    async def compress(self, ctx: commands.Context, *, data: str):
        """ Compress data with zlib (compression level 9). """
        compressed_data = zlib.compress(bytes(data, "utf-8"), 9)
        b64_text = base64.b64encode(compressed_data).decode("utf-8")

        embed = Crombed(
            title = "Compressed data",
            description = b64_text
        )

        await ctx.send(embed=embed)


    @commands.command()
    async def decompress(self, ctx: commands.Context, *, b64_text: str):
        """ Decompress base64-encoded, zlib-compressed data. """
        decoded = base64.b64decode(b64_text)
        decompressed = zlib.decompress(decoded).decode("utf-8")

        embed = Crombed(
            title = "Decompressed data",
            description = decompressed
        )

        await ctx.send(embed=embed)

    
    @commands.command(aliases=["b64e", "64e"])
    async def b64encode(self, ctx: commands.Context, *, data: str):
        """ Encode a string to base64. """
        b64_text = base64.b64encode(bytes(data, "utf-8")).decode("utf-8")

        embed = Crombed(
            title = "Base64 encoded data",
            description = b64_text
        )

        await ctx.send(embed=embed)


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

        await ctx.send(embed=embed)


    @commands.command(aliases=["picture", "photo", "photograph"])
    async def image(self, ctx: commands.Context, *, raw_text: str = None):
        """ Generate an image from text using the Text to Image API made by Scott Ellison Reed on deepai.org. """
        if raw_text:
            if is_mention(raw_text):
                # Evaluate mentions to nicknames
                user_id = extract_id(raw_text)
                processed_text = self.bot.get_user(user_id).display_name
            else:
                processed_text = raw_text
        else:
            processed_text = random_string(32)

        print(f"[garlic.py] Fetching an ooer image based on text \"{processed_text}\"...")

        response = requests.post(
            "https://api.deepai.org/api/text2img",
            data = {
                "text": processed_text,
            },
            headers = {
                "api-key": os.environ["DEEPAI_API_KEY"]
            }
        ).json()

        try:
            url = response["output_url"]
        except KeyError:
            raise Exception(f"Expected key 'output_url': {str(response)}")

        embed = Crombed(
            title = "Image",
            description = processed_text if raw_text else None, # Only show the text cromgis used if the text came from a user
            author = ctx.author
        ).set_image(url=url)

        await ctx.send(embed=embed)


    @commands.command(aliases=["mp4togif"])
    async def mp4togifv(self, ctx: commands.Context, mp4_url: str):
        gifv_url = imgur.upload_image(
            path=mp4_url,
            title="cromgis video (Uploaded with PyImgur)"
        ).link

        embed = Crombed(
            title = "GIF converted from MP4",
            url = gifv_url,
            author = ctx.author
        )

        await ctx.send(embed=embed)


    @commands.command(aliases=["gib", "gibber"])
    async def gibberish(self, ctx: commands.Context, *, text: str):
        level = random.randint(1, 6)
        length = random.randint(5, 750)
        gibberish_text = generate_gibberish(text, level, length)

        await ctx.send(gibberish_text)


    @commands.group()
    async def number(self, ctx: commands.Context):
        await self.next_number(ctx)


    @number.command(name="next")
    async def next_number(self, ctx: commands.Context):
        user_number = usernumber.generate(ctx.author.id)

        # Send out the generated number
        embed = Crombed(
            description = "Your next number is: " + user_number,
            author = ctx.author
        )
        await ctx.send(embed=embed)


    @number.command(name="current")
    async def current_number(self, ctx: commands.Context):
        counter = usernumber.get_counter(ctx.author.id)

        # Number suffix
        th = "th"
        if counter[-1] == 1:
            th = "st"
        elif counter[-1] == 2:
            th = "nd"
        elif counter[-1] == 3:
            th = "rd"
 
        # Send out the user's current counter
        embed = Crombed(
            description = f"You are currently on your {counter}{th} number.",
            author = ctx.author
        )
        await ctx.send(embed=embed)


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
        message_authorIDs = set()
        message_content = set()
        async for m in message.channel.history(limit=REPLY_CHAIN_LENGTH):
            """ Contribute to message chains """
            message_authorIDs.add(m.author.id)
            message_content.add(m.content)

        if self.bot.user.id in message_authorIDs:
            """ Do not reply to self """
            return

        if len(message_content) == 1 and len(message_authorIDs) >= REPLY_CHAIN_LENGTH:
            return await message.channel.send(message_content.pop())


        if chance(2):
            """ Chance to say a funny """
            function = random.choice([generate_scream, generate_screech, ooojoy])
            text = function()
            return await message.channel.send(text)

        if "AAA" in message.content.upper():
            """ Scream in response to screams """
            return await message.channel.send(generate_scream())
        
        if "EEE" in message.content.upper():
            """ Screech in response to screeches """
            return await message.channel.send(generate_screech())

        if "@someone" in message.content:
            """ @someone: ping random user """
            member = random.choice(message.channel.members)
            return await message.channel.send(f"<@{member.id}>")




def setup(bot):
    bot.add_cog(GarlicCommands(bot))
