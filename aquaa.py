import discord
from discord.ext import commands
class AquaaCommands(commands.Cog):
    """ Commands requested by aquaa """

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def ooo(self, ctx):
        # Say "ooo 😂" 
        await ctx.channel.send("ooo :joy:")
      
async def setup(bot):
    await bot.add_cog(AquaaCommands(bot))
