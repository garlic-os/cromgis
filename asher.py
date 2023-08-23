# Made on Asher's behalf by garlicOS®

from discord.ext import commands
import markovify
import random
import pickle


def make_proper_sentence(model: markovify.Text) -> str:
    """ Make sentences that start with a capital letter and end with a puncutation mark. """
    puncutation = [".", "?", "!"]
    sentence = model.make_sentence().capitalize()

    if sentence[-1] not in puncutation:
        sentence += random.choice(puncutation)

    return sentence

def make_paragraph(model: markovify.Text, sentence_count_goal: int) -> str:
    """ Generate a sequence of sentences. """
    MAX_LENGTH = 2000
    essay = make_proper_sentence(model)
    addition = make_proper_sentence(model)
    sentence_count = 0

    while sentence_count < sentence_count_goal and len(essay) + len(addition) < MAX_LENGTH:
        essay += " " + addition
        addition = make_proper_sentence(model)
        sentence_count += 1

    return essay


def regenerate() -> markovify.Text:
    """ Generate the asher model from asher-corpus.txt and cache it for next time """
    # Form a new model from the corpus file
    with open("asher-corpus.txt") as corpus_file:
        asher_markov = markovify.Text(corpus_file.read()).compile()
    # Pickle the new model
    with open("asher-model.pickle", "wb+") as model_file:
        pickle.dump(asher_markov, model_file)

    return asher_markov


try:
    # Reconstitute the pickled model, if it exists
    with open("asher-model.pickle", "rb") as model_file:
        print("[asher.py] Loading asher model from cache.")
        asher_markov = pickle.load(model_file)
except FileNotFoundError:
    print("[asher.py] Cached asher model not found. Regenerating from corpus.")
    asher_markov = regenerate()



class AsherCommands(commands.Cog):
    """ Commands made on Asher's behalf! """

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def essay(self, ctx: commands.Context, sentence_count_goal=5):
        """ Generate an Asherian essay. [sentences | \"max\"]"""
        await ctx.channel.typing()

        if sentence_count_goal == "max":
            sentence_count_goal = 500
        elif type(sentence_count_goal) != int:
            raise ValueError("Requested sentence count is neither a number nor \"max\"")

        await ctx.send(make_paragraph(asher_markov, sentence_count_goal))


    @commands.command()
    async def regenerateEssayModel(self, ctx: commands.Context):
        """ Reload the corpus and make the markov model over again. """
        regenerate()



async def setup(bot):
    await bot.add_cog(AsherCommands(bot))
