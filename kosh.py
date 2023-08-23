

from discord.ext import commands
import markovify
import random
import os
# import pickle


# def regenerate() -> markovify.Text:
#     """ Generate the asher model from kosh-corpus.txt and cache it for next time """
#     # Form a new model from the corpus file
#     with open("kosh-corpus.txt") as corpus_file:
#         kosh_markov = markovify.Text(corpus_file.read()).compile()
#     # Pickle the new model
#     with open("kosh-model.pickle", "wb+") as model_file:
#         pickle.dump(kosh_markov, model_file)

#     return kosh_markov


# try:
#     # Reconstitute the pickled model, if it exists
#     with open("kosh-model.pickle", "rb") as model_file:
#         print("[kosh.py] Loading kosh model from cache.")
#         kosh_markov = pickle.load(model_file)
# except FileNotFoundError:
#     print("[kosh.py] Cached kosh model not found. Regenerating from corpus.")
#     kosh_markov = regenerate()
    


class KoshCommands(commands.Cog):
    """ Commands made on Asher's behalf! """
    def __init__(self, bot):
        self.bot = bot
        self.models = {}
      

        # Make Markov models out of all the .txt files in the corpora/ folder
        self.load_folder("corpora")

        self.create_combined_model()


    def create_combined_model(self):
        """
        Create the special "all" model by combining of the other
        models into one.
        """
        models_minus_all = []
        for model_name, model in self.models.items():
            if model_name != "all":
                models_minus_all.append(model)
        # Pass a list of all the models to markovify, minus the "all"
        # model itself in case it's already been generated
        self.models["all"] = markovify.combine(models_minus_all)


    def load_folder(self, folder_name):
        """
        Create Markov models out of every .txt file in the given folder
        and add it to the models dictionary, naming the model after the
        the text file it came from.
        """
        for entry in os.listdir(folder_name):
            abs_path = os.path.join(folder_name, entry)
            if os.path.isfile(abs_path):
                filename, ext = os.path.splitext(entry)
                if ext == ".txt":
                    with open(abs_path) as f_corpus:
                        # Generate the Markov model
                        self.models[filename] = markovify.Text(f_corpus.read())#.compile()


    def make_proper_sentence(self, model: markovify.Text) -> str:
        """ Make sentences that start with a capital letter and end with a punctuation mark. """
        punctuation = (".", "?", "!")
        sentence = model.make_sentence().capitalize()
        if sentence[-1] not in punctuation:
            sentence += random.choice(punctuation)
        return sentence


    def make_paragraph(self, model: markovify.Text, sentence_count_goal: int) -> str:
        """ Generate a sequence of sentences. """
        MAX_LENGTH = 2000
        essay = self.make_proper_sentence(model)
        addition = self.make_proper_sentence(model)
        sentence_count = 0

        while sentence_count < sentence_count_goal and len(essay) + len(addition) < MAX_LENGTH:
            essay += " " + addition
            addition = self.make_proper_sentence(model)
            sentence_count += 1

        return essay


    @commands.command()
    async def essay(self, ctx: commands.Context, model_name: str = "asher-model.pickle"):
        """ Generate an Kosh-esque essay. [sentences | \"max\"]"""
        await ctx.channel.typing()
        model = self.models.get(model_name, None)
        if model is None:
            raise ValueError("Invalid model name")
        await ctx.send(self.make_paragraph(model, 5))



async def setup(bot):
    await bot.add_cog(KoshCommands(bot))