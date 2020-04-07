import discord
from discord.ext import commands

class LettersCmds(commands.Cog):

    @commands.command()  # use commands.command in a cog
    async def whois(self, ctx: commands.Context, who: discord.Member = None):
        """ Returns someone's nickname, or if none, their tag. """
        if who:
            name = who.display_name
        else:
            name = ctx.author.display_name
        await ctx.send(f"Why it's {name}, of course") 


    @commands.command()
    async def role(self, ctx, role: discord.Role = None):
        """ Returns info about a role. """
        if not role:
            await ctx.send('Please pong a role buddy oh friend')
        else:
            await ctx.send(str(role.color))
    

def setup(bot):
    bot.add_cog(LettersCmds(bot))
