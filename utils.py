import discord
import random
import string


class Crombed(discord.Embed):
    """
    A Discord Embed with extra features!
    Concept definitely not stolen from crimsoBOT's source code:
    https://github.com/crimsobot/crimsoBOT/blob/0bbe9d0847d169ff5d124c92f00c2e71127d021a/crimsobot/utils/tools.py
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.crombed_args = kwargs

        self.set_color_by_name()
        self.set_author_by_user()
        self.set_image_by_name()

        del self.crombed_args


    def set_color_by_name(self):
        """ Set the embed's color by color_name if color is not defined. """
        """ If neither are defined, default to flesh color. """
        if self.color: # Let color override color_name
            return

        colors = {
            "flesh": 0x98784C,
            "red":   0xD32F2F,
            "squid": 0xBEF4C3,
            "teal":  0x1EC9A1
        }

        color_name = self.crombed_args.get("color_name", "flesh")
        self.color = colors[color_name]


    def set_author_by_user(self):
        """ Set the embed's author by a DiscordUser. """
        author = self.crombed_args.get("author", None)

        if author:
            name = author.display_name
            icon_url = author.avatar_url_as(size=32)
            self.set_author(name=name, icon_url=icon_url)


    def set_image_by_name(self):
        """ Set the embed's image by the URL of the image. """
        url = self.crombed_args.get("image_url", None)

        if url:
            self.set_image(url=url)



def chance(percent: float) -> bool:
    """ Random outcome with a <percent>% chance of being True. """
    return random.random() < percent / 100


def is_mention(text: str) -> bool:
    """ Determine if a string is a user mention. """
    correct_beginning = text[:2] == "<@"
    not_emoji = ":" not in text
    not_channel = "#" not in text
    correct_ending = text[-1] == ">"
    return correct_beginning and not_emoji and not_channel and correct_ending


def extract_id(text: str) -> int:
    """ Get a Discord ID from a string. """
    # Note: this is quite possibly the worst way to do this
    output = ""
    for char in text:
        if char in string.digits:
            output += char
    return int(output)


def random_string(length: int = 32) -> str:
    """ Generate a string of random letters and numbers. """
    """ Pasted from https://pythontips.com/2013/07/28/generating-a-random-string/ """
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])
