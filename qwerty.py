import discord
import random
from discord.ext import commands
class QwertyCommands(commands.Cog):
    """ Commands made by QwertyDazerty! """

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def wheelofping(self, ctx: commands.Context):
        """ Pings a random user. pray that it doesn't ping a mod. """
        member_choices = [m for m in discord.guild.Guild.members 
				if (not m.bot)]
        member = random.choice(member_choices)
        return await discord.channel.send(member.mention)
    @commands.command()
    async def shlurp(self, ctx, human: discord.Member = None):
      """shlurp"""
      if human:
            await ctx.send(
                '> ' +
                ctx.message.author.mention +  
                ' has shlurped up' + human.mention + ". :yum:"
            )
def setup(bot):
  bot.add_cog(QwertyCommands(bot))
