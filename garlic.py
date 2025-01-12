import base64
import json
import os
import random
import zlib
from io import BytesIO, StringIO
from typing import cast
from urllib.parse import urlparse

import discord
import qrcode
from discord.ext import commands

from garlic_functions import ProbDist, humanize_text, run_bf, string_to_bf
from pxl_srt import pxl_srt
from utils import Crombed, chance, random_string

from .main import Cromgis


REPLY_CHAIN_LENGTH = int(os.environ["REPLY_CHAIN_LENGTH"])


class GarlicCommands(commands.Cog):
	"""Commands made by garlicOS®!"""

	def __init__(self, bot: Cromgis) -> None:
		self.bot = bot
		self.spoilerize_ai_images: bool = os.environ.get(
			"SPOILERIZE_AI_IMAGES", ""
		).lower() in ("true", "1")

	@commands.command(aliases=["meow", "nyan", "kitty", "kitten", "feline"])
	async def cat(self, ctx: commands.Context) -> None:
		"""Generate a cat from thiscatdoesnotexist.com."""
		url = f"https://thiscatdoesnotexist.com/?{random_string(32)}"

		embed = Crombed(title="Cat").set_image(url=url)

		await ctx.reply(embed=embed)

	# This code causes an error on thispersondoesnotexist's end.
	# If you know what I can do to fix this, please tell me

	# @commands.command(aliases=["face", "facereveal", "human"])
	# async def person(self, ctx: commands.Context):
	#     """ Generate a face from thispersondoesnotexist.com. """
	#     url = f"https://thispersondoesnotexist.com/image?{random_string(32)}"

	#     # This one does not seem to play nice with Discord like the other two do,
	#     #   so it requires a little finangling to get it to work.
	#     response = requests.get(url, stream = True)

	#     img = BytesIO(response.content)

	#     embed = Crombed(
	#         title = "Person",
	#         author = ctx.author,
	#         file = discord.File(img, filename="image.jpg")
	#     )

	#     await ctx.send(embed=embed)

	@commands.command()
	async def horse(self, ctx: commands.Context) -> None:
		"""Generate a horse from thishorsedoesnotexist.com."""
		url = f"https://thishorsedoesnotexist.com/?{random_string(32)}"

		embed = Crombed(title="Horse").set_image(url=url)

		await ctx.reply(embed=embed)

	@commands.command(aliases=["info", "source", "github"])
	async def code(self, ctx: commands.Context) -> None:
		"""Look at cromgis's code!"""
		embed = Crombed(
			title="Source code",
			description="cromgis is an open-source bot made by the /r/Ooer hivemind. See its code here:\nhttps://github.com/garlic-os/cromgis",
		)
		await ctx.reply(embed=embed)

	@commands.command(aliases=["ev"])
	async def expectedValue(
		self, ctx: commands.Context, *, json_data: str
	) -> None:
		"""Calculate the expected value of a probability distribution."""
		try:
			probabilities = json.loads(json_data)
		except json.decoder.JSONDecodeError:
			await ctx.reply("Syntax error")
			return

		prob_dist = ProbDist(probabilities)

		embed = Crombed(
			title="Expected value", description=str(prob_dist.expected_value)
		)
		await ctx.reply(embed=embed)

	@commands.command(aliases=["sd"])
	async def standardDeviation(
		self, ctx: commands.Context, *, json_data: str
	) -> None:
		"""Calculate the standard deviation of a probability distribution."""
		try:
			probabilities = json.loads(json_data)
		except json.decoder.JSONDecodeError:
			await ctx.reply("Syntax error")
			return

		prob_dist = ProbDist(probabilities)

		embed = Crombed(
			title="Standard deviation",
			description=str(prob_dist.standard_deviation),
		)
		await ctx.reply(embed=embed)

	@commands.command(aliases=["bf"])
	async def executeBF(self, ctx: commands.Context, *, data: str) -> None:
		"""Execute and print the output of a BF program."""
		program_out = run_bf(data)

		embed = Crombed(title="Brainfuck output", description=program_out)

		await ctx.reply(embed=embed)

	@commands.command()
	async def text2bf(self, ctx: commands.Context, *, text: str) -> None:
		"""Make a BF program that outputs the given text."""
		bf_program = string_to_bf(text)

		embed = Crombed(title="Brainfuck program", description=bf_program)

		await ctx.reply(embed=embed)

	@commands.command()
	async def compress(self, ctx: commands.Context, *, data: str) -> None:
		"""Compress data with zlib (compression level 9)."""
		compressed_data = zlib.compress(bytes(data, "utf-8"), 9)
		b64_text = base64.b64encode(compressed_data).decode("utf-8")

		embed = Crombed(title="Compressed data", description=b64_text)

		await ctx.reply(embed=embed)

	@commands.command()
	async def decompress(self, ctx: commands.Context, *, b64_text: str) -> None:
		"""Decompress base64-encoded, zlib-compressed data."""
		decoded = base64.b64decode(b64_text)
		decompressed = zlib.decompress(decoded).decode("utf-8")

		embed = Crombed(title="Decompressed data", description=decompressed)

		await ctx.reply(embed=embed)

	@commands.command(aliases=["b64e", "64e"])
	async def b64encode(self, ctx: commands.Context, *, data: str) -> None:
		"""Encode a string to base64."""
		b64_text = base64.b64encode(bytes(data, "utf-8")).decode("utf-8")
		embed = Crombed(title="Base64 encoded data", description=b64_text)
		await ctx.reply(embed=embed)

	@commands.command(aliases=["b64d", "64d"])
	async def b64decode(self, ctx: commands.Context, *, b64_text: str) -> None:
		"""Decode a base64-encoded string."""
		while len(b64_text) % 4 != 0:
			b64_text += "="
		decoded_data = base64.b64decode(b64_text).decode("utf-8")
		embed = Crombed(title="Base64 decoded data", description=decoded_data)
		await ctx.reply(embed=embed)

	@commands.command(aliases=["qrcode"])
	async def qr(self, ctx: commands.Context, *, data: str) -> None:
		"""Make a QR code"""
		qr = qrcode.QRCode()
		qr.add_data(data)
		buffer = StringIO()
		qr.print_ascii(out=buffer)
		buffer.seek(0)
		await ctx.reply(f"```\n{buffer.read()}\n```")

	@commands.command(
		aliases=["picture", "photo", "photograph"],
		enabled=False,  # API cost is too expensive now
	)
	@commands.cooldown(2, 4, commands.BucketType.user)
	async def image(
		self, ctx: commands.Context, *, text: str | None = None
	) -> None:
		"""
		Generate an image from text using the Text to Image API made by
		Scott Ellison Reed on deepai.org.
		"""
		prompt = humanize_text(ctx.message, text) if text else random_string(32)
		print(f'[garlic.py] Fetching an ooer image based on text "{prompt}"...')

		payload = {"text": prompt}
		headers = {"api-key": os.environ["DEEPAI_API_KEY"]}
		async with self.bot.http_session.post(
			"https://api.deepai.org/api/text2img", data=payload, headers=headers
		) as response:
			response = await response.json()

		try:
			url = response["output_url"]
		except KeyError:
			raise KeyError(f"Expected key 'output_url': {str(response)}")

		async with self.bot.http_session.get(
			url, data=payload, headers=headers
		) as response:
			image = BytesIO(await response.read())

		file_name = os.path.basename(urlparse(url).path)
		if self.spoilerize_ai_images:
			file_name = "SPOILER_" + file_name

		await ctx.reply(
			f"> **Image**\n> {text}",
			file=discord.File(image, filename=file_name),
		)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message) -> None:
		if self.bot.user.id == message.author.id:
			# Do not respond to self
			return

		message_author_ids = set()
		message_content = set()
		async for past_message in message.channel.history(
			limit=REPLY_CHAIN_LENGTH
		):
			if self.bot.user.id != past_message.author.id:
				# Contribute to message chains
				message_author_ids.add(past_message.author.id)
				message_content.add(past_message.content)

		if (
			len(message_content) == 1
			and len(message_author_ids) >= REPLY_CHAIN_LENGTH
		):
			await message.channel.send(message_content.pop())
			return

		if chance(2 / 3):
			# Chance to say ooo 😂
			await message.channel.send("ooo :joy:")
			return

		if "eggs benedict" in message.content.lower():
			# Say "ooo 😂" in response to "eggs benedict", per aquaa's request
			await message.channel.send("ooo :joy:")
			return

		if "@someone" in message.content:
			# @someone: ping random user
			random_member = random.choice(message.guild.members)
			await message.channel.send(random_member.mention)
			return

		PUPPET_STRING = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ ooer puppet "
		if PUPPET_STRING in message.content.lower():
			# Puppet: a special command wrapped inside hidden message that lets
			# you make the bot say whatever you want
			await message.channel.send(
				message.content.lower().split(PUPPET_STRING)[1]
			)
			return


async def setup(bot: Cromgis) -> None:
	await bot.add_cog(GarlicCommands(bot))
