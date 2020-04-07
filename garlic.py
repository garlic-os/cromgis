import discord
from discord.ext import commands
import random
import requests
from io import BytesIO

def chance(percent):
    return random.random() < percent / 100


def generateScream():
    # Vanilla scream half the time
    if chance(50):
        return "A" * random.randint(1, 100)
    
    # One of these choices repeated 1-100 times
    body = random.choice(["A", "O"]) * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put one of these at the end of the message
    suffix = "" if chance(50) else random.choice(["H", "ARGH"])

    text = formatter + body + formatter + suffix

    if chance(50):
        text = text.lower()

    return text


def allEqual(arr):
   return len(set(arr)) == 1
    

class GarlicCommands(commands.Cog):
    """ Commands made by garlicOS®! """

    lastFewMessages = [] # idk if this will work well see

    @commands.command()
    async def scream(self, ctx: commands.Context):
        """ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA """
        await ctx.send(generateScream())


    @commands.command()
    async def cat(self, ctx: commands.Context):
        """ Pull a cat from thiscatdoesnotexist.com. """        
        r = requests.get("https://thiscatdoesnotexist.com/")
        catFile = BytesIO(r.content)
        await ctx.send(file=discord.File(catFile, "cat.png"))


    @commands.Cog.listener()
    async def on_message(self, message):
        # Chance to scream in response to message
        if chance(5):
            text = generateScream() if chance(50) else "ooo :joy:"
            await message.channel.send(text)


        # Contribute to message chains
        self.lastFewMessages.append(message)
        if len(self.lastFewMessages) > 3:
            self.lastFewMessages.pop(0)

        for message in self.lastFewMessages:
            if 



def setup(bot):
    bot.add_cog(GarlicCommands(bot))
