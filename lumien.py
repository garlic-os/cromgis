import discord
from discord.ext import commands
import random
import io
import urllib.request


class LumienCommands(commands.Cog):
	"""Commands birthed by Lumien"""

	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["inspirobot", "inspiro", "inspiration"])
	async def inspire(self, ctx):
		"""Pulls a motivational image from inspirobot.me."""
		await ctx.channel.typing()
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
		api_url = "http://inspirobot.me/api?generate=true"
		path_response = urllib.request.urlopen(
			urllib.request.Request(api_url, headers={"User-Agent": user_agent})
		)
		image = urllib.request.urlopen(
			urllib.request.Request(
				path_response.read().decode("utf-8"),
				headers={"User-Agent": user_agent},
			)
		)
		data = io.BytesIO(image.read())
		await ctx.send(file=discord.File(data, "inspirobot.jpg"))

	@commands.command(aliases=["hug", "kiss", "consume", "destroy", "fluff"])
	async def interaction(self, ctx, victim: discord.User = None):
		"""hug | kiss | consume | destroy"""
		split = ctx.message.content.split(" ")
		if split[1] == "interaction":
			embed = discord.Embed(
				title=f"The following interactions are possible:",
				description="\nooer hug\nooer kiss\nooer consume\nooer destroy",
				color=0xFF48FF,
			).set_footer(text="Work in progress.")
			return await ctx.send(embed=embed)
		if victim == None:
			return await ctx.send("<:husk:697167137374208050>")
		alias_string_map = {
			"hug": f"**{ctx.author.display_name}** gives **{victim.display_name}** a hug! :heart:",
			"kiss": f"**{ctx.author.display_name}** kisses **{victim.display_name}**! :flushed:",
			"consume": f"**{ctx.author.display_name}** eats **{victim.display_name}** whole! :yum:",
			"destroy": f"**{ctx.author.display_name}** tears **{victim.display_name}** apart atom by atom! :atom:",
		}
		index = split[1]
		await ctx.send(alias_string_map[index])


async def setup(bot):
	await bot.add_cog(LumienCommands(bot))
