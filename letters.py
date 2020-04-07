import discord
from discord.ext import commands
import random as rand

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
    async def role(self, ctx, role: discord.Role):
        """ Returns info about a role. """
        embed = discord.Embed(
            title=role.name,
            color=role.color,
            description=f"Info for role *{role.name}*  ({role.id})"
        )
        embed.add_field(name='Hex color code', value=f"**{role.color}**")  # inline is true by default
        embed.add_field(name="Permission bitfield", value=role.permissions.value)
        members = ", ".join(str(m) for m in role.members) # no long line 
        embed.add_field(name="Members with this role", value=members)
        await ctx.send(embed=embed)

    @commands.command()
    async def emojis(self, ctx):
        """ Lists out all emojis in this guild. """
        await ctx.send("".join(str(e) for e in ctx.guild.emojis))
    
    @commands.command()
    async def randmoji(self, ctx):
        """ Gives a random emoji in this guild. """
        await ctx.send(rand.choice(ctx.guild.emojis))

    

def setup(bot):
    bot.add_cog(LettersCmds(bot))
