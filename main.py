# Join the Discord server we trapped the bot in!
# We'd post it on /r/Ooer but we'd get banned.
# https://discord.gg/GhptsGPd

from dotenv import load_dotenv
load_dotenv()

import logging
import os
import json
import random
from aiohttp import ClientSession
from utils import Crombed
from failure import failure_phrases
import discord
from discord.ext import commands
from discord.ext.commands.errors import (
    CommandError,
    CommandNotFound,
)

import badmarkov

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OoerBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_session = ClientSession()

    def __del__(self):
        self.http_session.close()

    async def on_message(self, message):
        if message.author.bot:  # this will catch webhooks as well iirc
            return
        if self.user.mentioned_in(message):
            # await message.channel.send(random.choice(pinged))
            await message.channel.send(self.markov.generate())

        await self.process_commands(message)

    async def on_command_error(self, ctx: commands.Context, exception: CommandError) -> None:
        # Ignore Command Not Found errors
        if type(exception) is CommandNotFound:
            return
        embed = Crombed(
            title = random.choice(failure_phrases),
            description = str(exception),
            color_name = "red"
        )
        await ctx.reply(embed=embed)
        print(f"\n{exception}\n")


print("Initializing bot...")
intents = discord.Intents.default()
intents.members = True

bot = OoerBot(
    command_prefix = (os.environ["COMMAND_PREFIX"], os.environ["COMMAND_PREFIX"].capitalize()),
    owner_ids = json.loads(os.environ["BOT_OWNERS"]),
    case_insensitive = True,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Game(name="Forged in steel and fire"),
    intents=intents,
)

bot.logger = logger
bot.markov = badmarkov.AwfulMarkov("markov_ooer", state_size=2)


@bot.event
async def on_ready():
    print("ooo online")


@bot.command()
async def ping(ctx):
    """ Respond with the bot's reponse time. """
    await ctx.send(f"Ping! Took **{round(bot.latency * 1000, 2)}** ms")

extensions = ["jishaku", 'letters', "delphi", "garlic", "asher", "lumien",
              "invalid", "garfield", "qwerty", "aquaa"]  # put this... somewhere, later
for extension in extensions:
    try:
        print(f"Loading extension {extension}...")
        bot.load_extension(extension)
        bot.logger.info(f"Loaded extension {extension}")
    except Exception as e:
        bot.logger.error(f"Failed to load extension {extension}; {e}")


print("Logging in...")
bot.run(os.environ["DISCORD_BOT_TOKEN"])
