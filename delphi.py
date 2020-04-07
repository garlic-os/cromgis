#These are for regular extensions
#do not run this file

if __name__ == "__main__":
	print("no")
	raise

import discord
from discord.ext import commands
import random

class DelphiCommands(commands.Cog):
    """docstring"""
    def __init__(self, bot):
        self.bot = bot

    #bless
    @commands.command()
    async def bless(self, ctx, human: discord.Member = None):
        if human:   
            await ctx.send(f"> {human.mention} has been <:bless:696879351333126245> **blessed** <:bless:696879351333126245>")
        else:
            await ctx.send('Bless who?')

    #blap
    @commands.command()
    async def blap(self, ctx, human: discord.Member = None):
        if human:   
            await ctx.send('> ' + human.mention + ' has been <:blap:685653048596758660> **BLAPPED** <:blap:685653048596758660>')
        else:
            await ctx.send('> ' + ctx.message.author.mention + ' has <:blap:685653048596758660> **BLAPPED** <:blap:685653048596758660> ')
    
    #rng
    @commands.command()
    async def rng(self, ctx, nu1: int = 5, nu2: int= 20): # defaults
        await ctx.send(random.randint(nu1, nu2))
        await ctx.send(random.randint(1, 100)) # default values 5 and 20 already do this?

    #get server icon
    @commands.command()
    async def icon(self, ctx):
        await ctx.send(ctx.guild.icon_url)

    #get your or someone else's avatar
    @commands.command()
    async def avatar(self, ctx, human: discord.Member = None):
      if human:   
        await ctx.send(human.avatar_url)
      else:
        await ctx.send(ctx.author.avatar_url)

    @commands.command()
    async def mindbreak(self, ctx):
        with open("mind.txt", encoding="utf8") as f:
             corpus = f.readlines()
        await ctx.send(" ".join(random.sample(corpus, 50)))

def setup(bot):
    bot.add_cog(DelphiCommands(bot))
