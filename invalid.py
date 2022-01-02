from discord.ext import commands
import random
import re
from utils import Crombed

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


  @commands.command(aliases=["bakaize, bakaify, bakize, bakify"])
  async def baka(self, ctx: commands.Context, *, text):
      """In case you needed an anime girl to say anything."""
      await ctx.send(bakaText(text))


def setup(bot):
    bot.add_cog(InvalidCommands(bot))
