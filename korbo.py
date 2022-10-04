import discord
import random
from discord.ext import commands


def getmembersinrole(ctx, role: discord.Role):
    return role.members


class KorboCommands(commands.Cog):
    """ Commands made by Korbo! """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wheelofping(self, ctx: commands.Context):
        """ Pings any online user with \"ping role\". """
        members = getmembersinrole(
            ctx, discord.utils.get(ctx.guild.roles, id=1003048661493743706))
        mchoices = [mbr for mbr in members if str(mbr.status) != "offline"]
        member = random.choice(mchoices)
        return await ctx.send(member.mention)

    @commands.command()
    async def shlurp(self, ctx, human: discord.Member = None):
        """ shlurps the victim. :yum: """
        if human:
            await ctx.send('> ' + ctx.message.author.mention +
                           ' has shlurped up' + human.mention + ". :yum:")


async def setup(bot):
    await bot.add_cog(KorboCommands(bot))
