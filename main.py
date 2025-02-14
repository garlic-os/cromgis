# Join the Discord server we trapped the bot in!
# We'd post it on /r/Ooer but we'd get banned.
# https://discord.gg/GhptsGPd

import asyncio
import json
import logging
import os
import random

import aiohttp
import asyncio_atexit
import discord
from discord.ext import commands
from discord.ext.commands.errors import (
	CommandError,
	CommandNotFound,
)
from dotenv import load_dotenv

from failure import failure_phrases

# import badmarkov
from garlikov import Garlikov
from utils import Crombed


load_dotenv()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Cromgis(commands.AutoShardedBot):
	http_session: aiohttp.ClientSession
	# markov: badmarkov.AwfulMarkov
	logger: logging.Logger

	def __init__(self):
		# self.markov = badmarkov.AwfulMarkov("markov_ooer", state_size=2)
		with open("garlikov.json") as f:
			self.garlikov = Garlikov(parsed_sentences=json.load(f))
		self.logger = logger

		self.logger.info("Initializing bot...")
		intents = discord.Intents.default()
		intents.members = True
		intents.message_content = True

		super().__init__(
			command_prefix=(
				os.environ["COMMAND_PREFIX"],
				os.environ["COMMAND_PREFIX"].capitalize(),
			),
			owner_ids=json.loads(os.environ["BOT_OWNERS"]),
			case_insensitive=True,
			allowed_mentions=discord.AllowedMentions.none(),
			activity=discord.Game(name="Forged in steel and fire"),
			intents=intents,
		)

	async def cleanup(self) -> None:
		if hasattr(self, "http_session"):
			await self.http_session.close()

	async def on_message(self, message: discord.Message) -> None:
		if message.author.bot:  # this will catch webhooks as well iirc
			return
		if self.user.mentioned_in(message):
			# await message.channel.send(self.markov.generate())
			await message.reply(self.garlikov.respond(message.content))

		await self.process_commands(message)

	async def on_command_error(
		self, ctx: commands.Context, exception: CommandError
	) -> None:
		# Ignore Command Not Found errors
		if type(exception) is CommandNotFound:
			return
		embed = Crombed(
			title=random.choice(failure_phrases),
			description=str(exception),
			color_name="red",
		)
		await ctx.reply(embed=embed)
		self.logger.error(f"\n{exception}\n")

	async def setup_hook(self) -> None:
		self.http_session = aiohttp.ClientSession(loop=self.loop)
		asyncio_atexit.register(self.cleanup, loop=self.loop)
		extensions = [
			"jishaku",
			"i3vie",
			"delphi",
			"garlic",
			"asher",
			"lumien",
			"invalid",
			"commics",
			"korbo",
			"aquaa",
			"imgur",
			"cheese",
		]  # put this... somewhere, later
		async with asyncio.TaskGroup() as tg:
			for extension in extensions:
				try:
					self.logger.info(f"Loading extension {extension}...")
					tg.create_task(bot.load_extension(extension))
				except Exception as e:
					bot.logger.error(
						f"Failed to load extension {extension}; {e}"
					)

	async def on_ready(self) -> None:
		self.logger.info("ooo online")


if __name__ == "__main__":
	print("Logging in...")
	bot = Cromgis()

	@bot.command()
	async def ping(ctx: commands.Context) -> None:
		"""Respond with the bot's reponse time."""
		await ctx.send(f"Ping! Took **{round(bot.latency * 1000, 2)}** ms")

	bot.run(os.environ["DISCORD_BOT_TOKEN"])
