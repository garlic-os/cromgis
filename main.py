# use the chat box its over there >>>

import logging
import os

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
        print("ooo bot running")

owners = [240987337209675776, 556614860931072012, 206235904644349953, 342828210209161227, 636797375184240640]  # temp thing 
bot = OoerBot(command_prefix=os.environ["COMMAND_PREFIX"], owner_ids=owners)
bot.logger = logger


@bot.event
async def on_ready():
    bot.logger.info("ooo bot online")


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

