import discord
from discord.ext import commands
import random
import requests
from io import BytesIO

class GarlicCommands(commands.Cog):
    """ Commands made by garlicOS® """

    @commands.command()
    async def scream(self, ctx: commands.Context):
        """ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA """
        await ctx.send("A" * random.randint(1, 100))

    @commands.command()
    async def cat(self, ctx: commands.Context):
        """ Pull a cat from thiscatdoesnotexist.com. """        
        r = requests.get("https://thiscatdoesnotexist.com/")
        catFile = BytesIO(r.content)
        await ctx.send(file=discord.File(catFile, "cat.png"))

        

def setup(bot):
    bot.add_cog(GarlicCommands(bot))
