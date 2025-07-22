import discord
from discord.ext import commands


class KorboCommands(commands.Cog):
	"""Commands made by Korbo!"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def shlurp(self, ctx, human: discord.Member | None = None):
		"""shlurps the victim. :yum:"""
		if human:
			await ctx.send(
				"> "
				+ ctx.message.author.mention
				+ " has shlurped up"
				+ human.mention
				+ ". :yum:"
			)

	@commands.command()
	async def ooo(self, ctx):
		# Say "ooo 😂"
		await ctx.channel.send("ooo :joy:")


async def setup(bot):
	await bot.add_cog(KorboCommands(bot))
