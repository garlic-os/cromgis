from discord.ext import commands
import markovify


# Wrapper that hard-caps the character limit at 2000 characters
class DiscordMarkov:
    def __init__(self, path):
        with open(path) as f:
            text = f.read()
        self.markov = markovify.NewlineText(text)  # NewlineText is probably best for this

    def generate(self):
        return self.markov.make_sentence(max_words=2000)

#asherMarkov = DiscordMarkov("asher.txt")
asherMarkov = DiscordMarkov("mind.txt")


class AsherCommands(commands.Cog):
    """ Commands made on Asher's behalf! """

    # def __init__(self, bot):
    #     self.bot = bot


    @commands.command()
    async def essay(self, ctx: commands.Context):
        """ Generate a short Asherian essay. """
        await ctx.channel.trigger_typing()
        await ctx.send(asherMarkov.generate())




def setup(bot):
    bot.add_cog(AsherCommands(bot))
