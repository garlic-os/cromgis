import discord
from discord.ext import commands
import random as rand
import secrets
import os
from io import BytesIO
import json
from scipy import io  # this is being read, imports scipy.io which allows to import wavfile
from scipy.io import wavfile
import numpy
import requests
from PIL import Image

async def commonColor(imgfile):
  """ Returns the 'most common color' of PIL image imgfile, downsized to 150x150 for performance. """
  temp = imgfile.resize(size=(150, 150))
  best = (0, (0, 0, 0))
  for tpl in temp.getcolors(150*150):
    if (tpl[0] > best[0]):
        best = tpl
  return best

class LettersCmds(commands.Cog):
    """ Commands made by letters """

    @commands.command()
    async def role(self, ctx, *, role: discord.Role):
        """ Returns info about a role. """
        embed = discord.Embed(
            title=role.name,
            color=role.color,
            description=f"Info for role *{role.name}*  ({role.id})")
        embed.add_field(
            name='Hex color code',
            value=f"**{role.color}**")  # inline is true by default
        embed.add_field(
            name="Permission bitfield", value=role.permissions.value)
        members = ", ".join(str(m) for m in role.members)  # no long line
        if len(members) > 200:
            members = len(role.members)
        embed.add_field(
            name="Members with this role", value=members, inline=False
        )  # no inline for this field as it could potentially be long
        await ctx.send(embed=embed)

    @commands.command()
    async def emojis(self, ctx):
        """ Lists out all emojis in this guild. """
        await ctx.send("".join(str(e) for e in ctx.guild.emojis))

    @commands.command()
    async def randmoji(self, ctx):
        """ Gives a random emoji that the bot has access to. """
        await ctx.send(rand.choice(ctx.bot.emojis))

    @commands.command()
    async def owners(self, ctx):
        """ Lists off all of the bot owners. """
        owners = json.loads(os.environ["BOT_OWNERS"])
        oemb = discord.Embed(
            title="Bot owners",
            description="Everyone who contributed to the bot:\n {0}".format(
                ",\n".join(str(ctx.bot.get_user(id)) for id in owners)),
            color=ctx.guild.me.color)
        await ctx.send(embed=oemb)

    @commands.command(aliases=['cryptorandom', 'crng', 'cryptographicallysecurerandomnumber'])
    async def securerandom(self, ctx, bytes: int = 2):
        """ Provide a cryptographically secure random number. Maximum is (bytes) x 255. """
        num = int(secrets.token_hex(nbytes=bytes), base=16)
        await ctx.send(num)

    @commands.command()
    async def roll(self, ctx, num: int = 1, sides: int = 6, extra: int = 0):
        """ Roll (num) dice, each with (sides) sides. You can also specify an advantage or disadvantage with (extra)."""
        sum = 0
        for n in range(0, num):
            sum = sum + rand.randint(1, sides)
        await ctx.send(
            f"Rolled *{num}* d*{sides}* dice... result: **{sum} & {extra} = {sum + extra}**"
        )

    @commands.command(aliases=["static", "noise"])
    async def whitenoise(self, ctx, length: int = 5,
                         samplingrate: int = 10000):
        """ Generates white noise from cryptographically secure random numbers. Very loud, so turn your audio down. Possibly a memetic hazard. Can be up to 100 seconds long with (lensec) argument. Set sampling rate between 4500 and 15000Hz with (samplingrate) arg."""
        if length > 100 or length < 1:
            return await ctx.send(
                'Audio cannot be longer than 100 seconds or shorter than 1.')
        if samplingrate > 15000 or samplingrate < 4500:
            return await ctx.send(
                'Sampling rate must be between 4500 and 15000Hz.')
        pcsmsg = await ctx.send('Processing... this may take a few minutes')
        bytelen = length * samplingrate
        ran = []
        buffer = BytesIO()
        for n in range(bytelen):
            ran.append(int(secrets.token_hex(nbytes=2), 16))
        bytes = numpy.array(
            ran, dtype=numpy.int8)  # we'll feed this to our wav file
        wavfile.write(buffer, samplingrate, bytes)  # this is a bad idea
        filename = f"whitenoise-{length}s-{secrets.token_hex(nbytes=15)}.wav"  # generate a unique filename
        await ctx.send(file=discord.File(fp=buffer, filename=filename))
        await pcsmsg.delete()

    @commands.command()
    async def imageinfo(self, ctx):
        try:
          img = ctx.message.attachments[0]
        except IndexError:
          return await ctx.send('No attachment provided.')
        temp = requests.get(img.url)
        try:
          imgfile = Image.open(BytesIO(temp.content))
        except OSError:
          return await ctx.send('Invalid image.')
        emb = discord.Embed(
          title = f'Image information for {img.filename}'
        )
        # --- get the common color as hex 123456(78 if alpha)
        comcol = await commonColor(imgfile)
        ccolor = comcol[1]
        if len(ccolor) == 4:
          ccolor = '%02x%02x%02x%02x' % ccolor
        else:
          ccolor = '%02x%02x%02x' % ccolor
        # ---------------------------------------------------
        if ccolor == "00000000":
          ccolor = "Transparent"
        emb.add_field(name="Format", value=imgfile.format)
        res = imgfile.size
        emb.add_field(name="Resolution", value=f"{res[0]} \u00D7 {res[1]}")
        emb.add_field(name="Color mode", value=imgfile.mode)
        emb.color = discord.Colour.from_rgb(comcol[1][0], comcol[1][1], comcol[1][2])
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(LettersCmds(bot))
