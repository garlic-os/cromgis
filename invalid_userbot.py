import discord
from discord.ext import commands
from discord.utils import get
import re
import random
from invalid import replaceMessage
from gibberish import generate_gibberish

helpMessage = "```bash\nHere is a list of my commands!\n\nhelp - displays this message.\nsay, [text] - makes me say something.\n```"

async def botMessage (channel: discord.channel, content: str, nick: str, pfp: str):
  hooks = await channel.webhooks()
  hook = get(hooks, name="cromHook_bot") # check if webhook exists
  if not hook:
    hook = await channel.create_webhook(name="cromHook_bot") # create webhook
    # this does not check if the bot has permission to query/create webhooks and will raise an exception otherwise
  await hook.send(content=content, username=nick, avatar_url=pfp)


class UserBotCommands(commands.Cog):

  @commands.Cog.listener()
  async def on_message(self, message):

    cFile = open("botUsers.txt", "r")
    bots = [line.rstrip() for line in cFile]
    cFile.close()


    if str(message.author.id) not in bots:
      for user in message.mentions:
        if user != message.author:
          if str(user.id) in bots:
            command = re.sub('<@!?' + str(user.id) + '>[ ]?', '', message.content).split(",")

            text = "```bash\nERROR: Command \"" + command[0].lower() + "\" is not found.```"
            if command[0].lower() == "help":
              text = helpMessage
              
            elif command[0].lower() == "say":
              text = "```bash\n" + command[1] + "```"

            await botMessage(message.channel, text, user.display_name + "Bot", user.avatar_url)
    else:
      username = message.author.display_name + "Bot"
      text = '```bash\n' + re.sub("[`]", "", message.content) + '```'
      await replaceMessage(message, text, username)

              
async def setup(bot):
    await bot.add_cog(UserBotCommands(bot))