import discord
import random
from discord.ext import commands
from discord.utils import get
ping_role = 930603605344542770
role = get(guild.roles, id=ping_role)
class QwertyCommands(commands.Cog):
    """ Commands made by QwertyDazerty! """

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def wheelofping(self, ctx: commands.Context):
        """ Pings a user with the role "ping role." """
        random_member = random.choice(role.members)
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
