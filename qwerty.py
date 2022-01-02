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
        random_member = random.choice(ctx.guild.members)
        return await ctx.channel.send(random_member.mention)
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