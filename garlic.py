from discord.ext import commands
import random

def chance(percent):
    return random.random() < percent / 100


def generateScream():
    # Vanilla scream half the time
    if chance(50):
        return "A" * random.randint(1, 100)
    
    # One of these choices repeated 1-100 times
    body = random.choice(["A", "O"]) * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put one of these at the end of the message
    suffix = "" if chance(50) else random.choice(["H", "ARGH"])

    text = formatter + body + suffix + formatter

    if chance(50):
        text = text.lower()

    return text


def allEqual(arr):
   return len(set(arr)) == 1

def allUnique(arr):
    return len(set(arr)) == len(arr)

class GarlicCommands(commands.Cog):
    """ Commands made by garlicOS®! """

    # def __init__(self, bot):
    #     self.bot = bot


    @commands.command()
    async def scream(self, ctx: commands.Context):
        """ AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA """
        await ctx.send(generateScream())


    @commands.command()
    async def cat(self, ctx: commands.Context):
        """ Pull a cat from thiscatdoesnotexist.com. """        
        await ctx.send(f"https://thiscatdoesnotexist.com/?{random.randint(1000000000000000000000000000000, 9999999999999999999999999999999)}")


    @commands.command()
    async def code(self, ctx: commands.Context):
        """ View and edit cromgis's code! """
        await ctx.send("cromgis is a bot made by /r/Ooer, where we believe everyone has someone to contribute. Therefore, cromgis is open source! Join the IDE that it's running on and add your own code!\nhttps://repl.it/join/uedbezcr-garlic_os")


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Contribute to message chains
        message_history = await message.channel.history(limit=3).flatten()
        if self.bot.user in [m.author for m in message_history]:
            return
        
        message_content = set(m.content for m in message_history)
        if len(message_content) == 1:
            await message.channel.send(list(message_content)[0])


        # Chance to scream in response to message
        if chance(5) or "AAA" in message.content:
            text = generateScream() if chance(50) else "ooo :joy:"
            await message.channel.send(text)
        




def setup(bot):
    bot.add_cog(GarlicCommands(bot))
