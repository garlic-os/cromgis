import discord
from discord.ext import commands
from discord.utils import get
import random
import re
import string
import json
from utils import Crombed
from failure import failure_phrases
# from main import bot

def vending_machine():
    with open("vendingmachine.txt", "r") as vending_machine_file:
        the_prize = random.choice(vending_machine_file.readlines())

    return the_prize

userRandom = random.Random()

v_titles = [
    "Your prize!", "A gift for you...", "Ooh!", "Exciting!", "The vending machine bestows you an offering.", 
    "Thrilling!", "Amazing!", "Hmmm...", "What?", "Nice.", "That's remarkable!", "Sweet!"
]

uwuFace = ['owo', 'uwu', 'x3', '>.<', '>w<', '=w=', '=3=', '>3<', 'uwo']
uwuPunc = ['', '~', ' @@󺘆@@@', ' ````󺘆@``']
uwuPuncU = ['', '~']
uwuSounds = ['nya', 'reowr', 'mrowr', 'mreowr', 'meowr', 'meow', 'mrow']
uwuSniffs = [' cutewy*', ' pwayfuwwy*', ' wuvingwy*', ' cuwiouswy*', '*']
uwuNuzzles = [' cutewy*', ' pwayfuwwy*', ' wuvingwy*', '*']
  # yes, that is a private use area character, u+fa606. being used because the likelyhood that anybody's going to use that character on a discord server for any reason are very low, especially when it's enclosed in @ symbols like that (basically ignore the bug by making it so obscure nobody will find it :cousinbotto:)
bakaEnds = ['~', '~', ', b-baka!', ', b-b-baka!', ' uwu~']
bakaFaces = ['(  ⸲⸲◕ ̭ ◕⸴⸴)', '( ⸲⸲◕   ᳕◕⸴⸴)', '( ⸲⸲՛◕ ̭ ◕՝⸴⸴)', '>.<']

uwu_mapping = {
    '(?:r|l)': "w",
    '(?:R|L)': "W",
    '(?P<ca>[NGng])(?P<e>[aeiou])': '\g<ca>y\g<e>',
    '(?P<ca>[NG])(?P<h>[AEIOU])': 'NY\g<h>',
    '(?P<r>[Nn])[Yy](?P<s>[Ee])(?P<t>[\s!?.,~\'"])': '\g<r>\g<s>\g<t>',
    '(?P<a>\A|\s)the(?P<b>$|\s)': '\g<a>da\g<b>',
    '(?P<a>\A|\s)T[Hh]e(?P<b>$|\s)': '\g<a>Da\g<b>',
    '(?P<a>\A|\s)THE(?P<b>$|\s)': '\g<a>DA\g<b>',
    '(th)': 'd',
    '(T[Hh])': 'D',
    '(?P<i>(?<![PKVBMTpkvbmt])[PKVBMTpkvbmt]{1,1}?)(?P<j>[AEIOUaeiou])': '\g<i>w\g<j>',
    "(?P<k>[AEIOUaeiou])v[Ee]": "\g<k>v",
    "(?P<m>[AEIOUaeiou])V[Ee]": "\g<m>V",
    "[Oo]v[Ee]": "uv",
    "[Oo]V[Ee]": "UV",
    "(?P<n>[AEOUaeou])(?P<o>[PBTGXpbtgx])(?P<q>$|[\s!?.,~'\"])": "\g<n>\g<o>\g<o>o\g<q>",
    "(?P<c>[gG][yY][eE][tT])[tT][oO]": "\g<c>"
}

def uwuizeText (text: str):
    for k, v in uwu_mapping.items():
        text = re.sub(k, v, text)

    text = text + random.choice(uwuPunc) + " " + random.choice(uwuFace)
    text = re.sub("([\s!.～~])@@󺘆@@@", "... " + random.choice(uwuSounds) + "~", text)
    text = re.sub("[?]@@󺘆@@@", "...? " + random.choice(uwuSounds) + "~", text)
    q = random.choice(["n", "s", ""])
    if q == "n":
      text = re.sub("([\s!.～~])````󺘆@``", "~ *nyuzzewes u" + random.choice(uwuNuzzles), text)
      text = re.sub("@@󺘆@@@", random.choice(uwuSounds), text)
      text = re.sub("````󺘆@``", "... *nyuzzewes u" + random.choice(uwuNuzzles), text)
    elif q == "s":
      text = re.sub("([\s!.～~])````󺘆@``", "~ *snyiffs u" + random.choice(uwuSniffs), text)
      text = re.sub("@@󺘆@@@", random.choice(uwuSounds), text)
      text = re.sub("````󺘆@``", "... *snyiffs u" + random.choice(uwuSniffs), text)
    else:
      text = re.sub("([\s!.～~])````󺘆@``", "~ *pwuwws" + random.choice(uwuNuzzles), text)
      text = re.sub("@@󺘆@@@", random.choice(uwuSounds), text)
      text = re.sub("````󺘆@``", "... *pwuwws" + random.choice(uwuNuzzles), text)
    return text

def uwuizeUsername (text: str):
    for k, v in uwu_mapping.items():
        text = re.sub(k, v, text)
    userRandom.seed(text)
    return text + userRandom.choice(uwuPuncU) + " " + userRandom.choice(uwuFace)

def uwuizeU (user: str):
  f = open("uwuizedUsers.txt", "r")
  u = [q.rstrip() for q in f]
  f.close()
  if user in u:
    f = open("uwuizedUsers.txt", "w")
    for i in u:
      if i.strip("\n") != user:
        f.write(i + "\n")
    f.truncate()
    f.close()
  else:
    f = open("uwuizedUsers.txt", "a")
    f.write(user + "\n")
    f.close

with open("asherisms.json", "r") as e:
  asherisms_dictionary = json.load(e)

# asher = bot.get_user(286883056793681930)

def asherizeUser (user: str):
  f = open("asherizedUsers.txt", "r")
  ashers = [q.rstrip() for q in f]
  f.close()
  if user in ashers:
    f = open("asherizedUsers.txt", "w")
    for i in ashers:
      if i.strip("\n") != user:
        f.write(i + "\n")
    f.truncate()
    f.close()
  else:
    f = open("asherizedUsers.txt", "a")
    f.write(user + "\n")
    f.close

def bakaText (text: str):
  text2 = re.split(r'\b', text)
  ret = ""
  end = random.choice(bakaEnds)
  
  for i in text2:
    if (random.randint(0, 2) == 1) or (len(text2) < 3):
      ret += re.sub(r'(?P<a>\b[a-zA-Z])', r"\g<a>-" * random.randint(1,2) + r'\g<a>', i)
    else:
      ret += i
  ret = re.sub(r'[.]*\Z', "", ret)
  ret = re.sub(r'(?P<a>[!?]*)\Z', end + r"\g<a>", ret)
  
  if random.randint(0, 2) == 1:
    ret += " " + random.choice(bakaFaces)
  
  return ret

def bakaUser (user: str):
  f = open("bakaUsers.txt", "r")
  anime_people = [q.rstrip() for q in f]
  f.close()
  if user in anime_people:
    f = open("bakaUsers.txt", "w")
    for i in anime_people:
      if i.strip("\n") != user:
        f.write(i + "\n")
    f.truncate()
    f.close()
  else:
    f = open("bakaUsers.txt", "a")
    f.write(user + "\n")
    f.close



async def replaceMessage (message: discord.Message, content: str, nick: str):
  hooks = await message.channel.webhooks()
  hook = get(hooks, name="cromHook_imitate") # check if webhook exists
  if not hook:
    hook = await message.channel.create_webhook(name="cromHook_imitate") # create webhook
    # this does not check if the bot has permission to query/create webhooks and will raise an exception otherwise

  await message.delete()
  pfp = message.author.avatar_url
  await hook.send(content=content, username=nick, avatar_url=pfp)


class InvalidCommands(commands.Cog):
  """Commands made by Invalid."""

  @commands.command(aliases=["vending", "vm"])
  async def vendingmachine(self, ctx: commands.Context):
      """Get something from the vending machine!"""
      # with help from lumien

      iemb = Crombed(
        title = random.choice(v_titles),
        description = vending_machine(),
        color_name = "teal"
      )
      await ctx.send(embed=iemb)


  @commands.command(aliases=["uwu", "owo", "owoize", "uwuify", "owoify"])
  async def uwuize(self, ctx: commands.Context, *, text):
      """UwUize some text."""
      await ctx.send(uwuizeText(text))

  @commands.command(aliases=["uwume", "owome", "owoizeme", "uwuifyme", "owoifyme"])
  async def uwuizeme(self, ctx: commands.Context):
      """UwUizes/de-uwuizes you.""" # this used to be able to target other users but i think that could be abused
      uwuizeU(str(ctx.message.author.id))

  @commands.command(aliases=["asherifyme", "asherme"])
  async def asherizeme(self, ctx: commands.Context):
      """Asherizes/de-asherizes you, making you speak in asherisms."""
      if not str(ctx.message.author.id) == "286883056793681930":
        asherizeUser(str(ctx.message.author.id))
      else:
        embed = Crombed(
            title = random.choice(failure_phrases),
            description = "You are already Asher. It is impossible for you to use this. If you did, it would annihilate you.",
            color_name = "red",
            author = ctx.author
        )
        await ctx.send(embed=embed)

  @commands.command(aliases=["bakaize, bakaify, bakize, bakify"])
  async def baka(self, ctx: commands.Context, *, text):
      """In case you needed an anime girl to say anything."""
      await ctx.send(bakaText(text))

  @commands.command(aliases=["bakaizeme, bakaifyme, bakizeme, bakifyme"])
  async def bakame(self, ctx: commands.Context):
      """Or you want to be the anime girl, for some reason."""
      bakaUser(str(ctx.message.author.id))

  @commands.Cog.listener()
  async def on_message(self, message):
    cFile = open("asherizedUsers.txt", "r")
    asher = [line.rstrip() for line in cFile]
    cFile.close()

    cFile = open("uwuizedUsers.txt", "r")
    uwu = [line.rstrip() for line in cFile]
    cFile.close()

    cFile = open("bakaUsers.txt", "r")
    baka = [line.rstrip() for line in cFile]
    cFile.close()

    if str(message.author.id) in asher:
      text = message.content
      words = [word.translate(str.maketrans("", "", string.punctuation)) for word in message.content.split(" ")]
      for word in words:
        asherisms = asherisms_dictionary.get(word, [[word]])[0]  # will look for asherised word, otherwise return list containing base word
        text = text.replace(word, random.choice(asherisms))

      ausername = "Asher (not " + message.author.display_name + ')'
      await replaceMessage(message, text, ausername)

    elif str(message.author.id) in uwu:
      text = uwuizeText(message.content)
      ausername = uwuizeUsername(message.author.display_name)
      await replaceMessage(message, text, ausername)

    elif str(message.author.id) in baka:
      text = bakaText(message.content)
      ausername = message.author.display_name + "-chan"
      await replaceMessage(message, text, ausername)

  # didn't know how to make user mindbreak :(
  
  




def setup(bot):
    bot.add_cog(InvalidCommands(bot))
