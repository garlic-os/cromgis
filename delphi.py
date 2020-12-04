if __name__ == "__main__":
    print("no")
    raise

import discord
from discord.ext import commands
import random
import asyncio
import insult



class DelphiCommands(commands.Cog):
    """docstring"""

    def __init__(self, bot):
        self.bot = bot

    #bless
    @commands.command()
    async def bless(self, ctx, human: discord.Member = None):
        """Bless a person."""
        if human:
            await ctx.send(
                f"> {human.mention} has been <:bless:696879351333126245> **blessed** <:bless:696879351333126245>"
            )
        else:
            await ctx.send('Bless who?')

    #blap
    @commands.command()
    async def blap(self, ctx, human: discord.Member = None):
        """BLAP SOMEONE."""
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
    async def rng(self, ctx, nu1: int = 1, nu2: int = 100): # defaults 1 & 100
        """Simple random number generator."""
        await ctx.send(random.randint(nu1, nu2))
    
    #get server icon
    @commands.command()
    async def icon(self, ctx):
        """Returns the server's icon."""
        iemb = discord.Embed(
            title=f"Guild icon for {ctx.guild.name}",
            color=0xBEF4C3
        )
        iemb.set_image(url=ctx.guild.icon_url)
        await ctx.send(embed=iemb)

    #get your or someone else's avatar
    @commands.command()
    async def avatar(self, ctx, human: discord.Member = None):
        """Returns a user's avatar."""
        mem = (human or ctx.author)
        aemb = discord.Embed(
            title=f"Avatar for {mem}",
            color=0xBEF4C3
        )
        aemb.set_image(url=mem.avatar_url)
        await ctx.send(embed=aemb)




    @commands.command()
    async def mindbreak(self, ctx):
        """Don't."""
        Exclamation = "!" * random.randint(1, 35)
        with open("mind.txt", encoding="utf8") as f:
            corpus = f.read()
        corpus = corpus.split(" ")
        await ctx.send("**" + " ".join(random.sample(corpus, 25)) + Exclamation + "**")

    @commands.command(enabled=False)
    async def insult(self, ctx):
        """Insults you."""
        choice1 = random.choice(insult.item1)
        choice2 = random.choice(insult.item2)
        choice3 = random.choice(insult.item3)

        if choice1[-1] == "a" and choice2[-1] in "aeiou":
            choice1 += "n"

        await ctx.send(f"{choice1} {choice2} {choice3}")



def setup(bot):
    bot.add_cog(DelphiCommands(bot))
