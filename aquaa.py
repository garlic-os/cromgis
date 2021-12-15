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
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id = 116275390695079945;
            # Do not respond to self
            return await message.channel.send("stfu nadeko")
def setup(bot):
    bot.add_cog(AquaaCommands(bot))
