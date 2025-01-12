import discord
import random
from discord.ext import commands


class KorboCommands(commands.Cog):
	"""Commands made by Korbo!"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def shlurp(self, ctx, human: discord.Member = None):
		"""shlurps the victim. :yum:"""
		if human:
			await ctx.send(
				"> "
				+ ctx.message.author.mention
				+ " has shlurped up"
				+ human.mention
				+ ". :yum:"
			)


async def setup(bot):
	await bot.add_cog(KorboCommands(bot))
