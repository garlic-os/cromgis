# Join the Discord server we trapped the bot in! We'd post it on /r/Ooer but we'd get banned.
# https://discord.gg/pKGBpA

import logging
import os
import json

import jishaku
import discord  # may be not-needed, we'll see
from discord.ext import commands  # should be all we need, depends

logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO)

class OoerBot(commands.AutoShardedBot):
    # i just realized there's basically no reason to subclass but w/e

    async def on_message(self, message):
        if message.author.bot:  # this will catch webhooks as well iirc
            return

        await self.process_commands(message)

    async def on_command_error(self, ctx, exception):
        await ctx.send(f"you are suck; {exception}")
    async def on_ready(self):
        print("why doesn't this code run")  # it's because it's not registered as an event

bot = OoerBot(
    command_prefix=os.environ["COMMAND_PREFIX"],
    owner_ids=json.loads(os.environ["BOT_OWNERS"]),
    case_insensitive=True
)
bot.logger = logger


@bot.event
async def on_ready():
    bot.logger.info("ooo bot online")  # this *should* run


@bot.command()
async def ping(ctx):
    """Responds with the bot's ping"""
    await ctx.send(f"Ping! Took **{round(bot.latency * 1000, 2)}** ms")

extensions = ['letters', "delphi", "garlic", "jishaku"]  # put this... somewhere, later
for extension in extensions:
    try:
        bot.load_extension(extension)
        bot.logger.info(f"Loaded extension {extension}")
    except Exception as e:
        bot.logger.error(f"Failed to load extension {extension}; {e}")


bot.run(os.environ["DISCORD_BOT_TOKEN"])

