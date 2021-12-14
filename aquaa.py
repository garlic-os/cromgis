import discord
from discord.ext import commands
class AquaaCommands(commands.Cog):
    """ Commands requested by aquaa """

    def __init__(self, bot):
        self.bot = bot
    @commands.command(ailises=["ooo"])
    # Say "ooo 😂" 
        await message.channel.send("ooo :joy:")
      
def setup(bot):
    bot.add_cog(AquaaCommands(bot))
