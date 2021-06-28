# Join the Discord server we trapped the bot in!
# We'd post it on /r/Ooer but we'd get banned.
# https://discord.gg/pKGBpA

from dotenv import load_dotenv
load_dotenv()

import logging
import os
import json
import random
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
    # i just realized there's basically no reason to subclass but w/e

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
        logger.error(f"\n{exception}\n")


print("Initializing bot...")
bot = OoerBot(
    command_prefix = (os.environ["COMMAND_PREFIX"], os.environ["COMMAND_PREFIX"].capitalize()),
    owner_ids = json.loads(os.environ["BOT_OWNERS"]),
    case_insensitive = True,
    allowed_mentions=discord.AllowedMentions.none(),
    activity=discord.Game(name="Forged in steel and fire"),
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

extensions = ["jishaku", 'letters', "delphi", "garlic", "asher", "lumien", "invalid", "garfield"]  # put this... somewhere, later
for extension in extensions:
    try:
        print(f"Loading extension {extension}...")
        bot.load_extension(extension)
        bot.logger.info(f"Loaded extension {extension}")
    except Exception as e:
        bot.logger.error(f"Failed to load extension {extension}; {e}")


print("Logging in...")
bot.run(os.environ["DISCORD_BOT_TOKEN"])
