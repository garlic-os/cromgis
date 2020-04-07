#These are for regular extensions
#do not run this file

if __name__ == "__main__":
    print("no")
    raise

import discord
from discord.ext import commands
import random
import asyncio


class DelphiCommands(commands.Cog):
    """docstring"""

    def __init__(self, bot):
        self.bot = bot

    #bless
    @commands.command()
    async def bless(self, ctx, human: discord.Member = None):
        if human:
            await ctx.send(
                f"> {human.mention} has been <:bless:696879351333126245> **blessed** <:bless:696879351333126245>"
            )
        else:
            await ctx.send('Bless who?')

    #blap
    @commands.command()
    async def blap(self, ctx, human: discord.Member = None):
        if human:
            await ctx.send(
                '> ' + human.mention +
                ' has been <:blapst:696885924411473940> **BLAPPED** <:blapst:696885924411473940>'
            )
        else:
            await ctx.send(
                '> ' + ctx.message.author.mention +
                ' has <:blapst:696885924411473940> **BLAPPED** <:blapst:696885924411473940> '
            )

    #rng
    @commands.command()
    async def rng(self, ctx, nu1: int = 5, nu2: int = 20):  # defaults
        await ctx.send(random.randint(nu1, nu2))
        await ctx.send(random.randint(
            1, 100))  # default values 5 and 20 already do this?
    
    #get server icon
    @commands.command()
    async def icon(self, ctx):
        iemb = discord.Embed(
            title=f"Guild icon for {ctx.guild.name}",
            color=15073280
        )
        iemb.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=iemb)

    #get your or someone else's avatar
    @commands.command()
    async def avatar(self, ctx, human: discord.Member = None):
        mem = (human or ctx.author)
        aemb = discord.Embed(
            title=f"Avatar for {mem}",
            color=15073280
        )
        aemb.set_image(url=mem.avatar_url)
        await ctx.send(embed=aemb)

    @commands.command()
    async def mindbreak(self, ctx):
        """don't"""
        with open("mind.txt", encoding="utf8") as f:
            corpus = f.read()
        corpus = corpus.split(" ")
        await ctx.message.channel.trigger_typing()
        await asyncio.sleep(random.randint(1, 2))
        await ctx.send("**" + " ".join(random.sample(corpus, 25)) + "**")


def setup(bot):
    bot.add_cog(DelphiCommands(bot))
