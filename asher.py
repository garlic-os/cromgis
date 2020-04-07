from discord.ext import commands
import markovify


def makeMarkov(path):
    with open("asher.txt") as f:
        text = f.read()
asherMarkov = markovify.Text(text)



class AsherCommands(commands.Cog):
    """ Commands made on Asher's behalf! """

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def essay(self, ctx: commands.Context):
        """ Generate a short essay. """
        await ctx.send(asherMarkov.make_sentence(2000))




def setup(bot):
    bot.add_cog(AsherCommands(bot))
