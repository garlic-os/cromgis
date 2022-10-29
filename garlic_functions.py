from discord import Message
from utils import chance
import random
import nbfi
import base64
import zlib
import requests
import re


def generate_scream() -> str:
    # Vanilla scream half the time
    if chance(50):
        return "A" * random.randint(1, 100)

    # One of these choices repeated 1-100 times
    body = random.choice(["A", "O"]) * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put one of these at the end of the message
    suffix = "" if chance(50) else random.choice(["H", "RGH"])

    # Example: "**AAAAAAAAAAAARGH**"
    text = formatter + body + suffix + formatter

    if chance(50):
        text = text.lower()

    return text


def generate_screech() -> str:
    # Vanilla screech half the time
    if chance(50):
        return "E" * random.randint(1, 100)

    # One of these choices repeated 1-100 times
    body = "E" * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put an "R" at the beginning of the message
    prefix = "" if chance(50) else "R"

    # Example: "**REEEEEEEEEEEEEEEEEEE**"
    text = formatter + prefix + body + formatter

    if chance(50):
        text = text.lower()

    return text


def ooojoy() -> str:
    return "ooo :joy:"



class ProbDist:
    def __init__(self, probabilities):
        self.probs = {}
        for key in probabilities:
            self.probs[float(key)] = probabilities[key]


    @property
    def expected_value(self):
        """ μ = Σ(xP(x)) """
        ev = 0

        for key in self.probs:
            ev += key * self.probs[key]

        return ev


    @property
    def standard_deviation(self):
        """ σ = sqrt(Σ(x-μ)^2 P(x)) """
        sd = 0

        for key in self.probs:
            sd += (key - self.expected_value) ** 2 * self.probs[key]

        return sd ** (1 / 2)


# Patch for nbfi that prevents it from printing values to console
def __execute(code: list, stackSize: int) -> list:
    """Run BF code"""
    iptr = 0
    sptr = 0
    output = ""
    stack = list(0 for _ in range(stackSize))
    codeLen = len(code)

    while iptr < codeLen:
        instruction = code[iptr][0]
        if instruction == ">":
            sptr += 1
        elif instruction == "<":
            sptr -= 1
        elif instruction == "+":
            stack[sptr] += 1
            if stack[sptr] == 256:
                stack[sptr] = 0
        elif instruction == "-":
            stack[sptr] -= 1
            if stack[sptr] == -1:
                stack[sptr] = 255
        elif instruction == ".":
            output += chr(stack[sptr])  # MODIFIED HERE: No more printing for you!
        elif instruction == ",":
            stack[sptr] = nbfi.__getchar()
        elif instruction == "[" and stack[sptr] == 0:
            iptr = code[iptr][1]
        elif instruction == "]" and stack[sptr] != 0:
            iptr = code[iptr][1]
        iptr += 1

    nbfi.__getchar.stdin_buffer = []
    return output


nbfi.__execute = __execute


def string_to_bf(source_string):
    """Convert a string into a BF program. Returns the BF code"""
    """Thanks, yiangos on GitHub."""
    glyphs = len(set([c for c in source_string]))
    number_of_bins = max(max([ord(c) for c in source_string]) // glyphs, 1)
    bins = [(i + 1) * number_of_bins for i in range(glyphs)]
    code = "+" * number_of_bins + "["
    code += "".join([">" + ("+" * (i + 1)) for i in range(1, glyphs)])
    code += "<" * (glyphs - 1) + "-]"
    code += "+" * number_of_bins
    current_bin = 0

    for char in source_string:
        new_bin = [abs(ord(char) - b)
            for b in bins].index(min([abs(ord(char) - b)
                for b in bins]))
        appending_char = ""
        if new_bin - current_bin > 0:
            appending_char = ">"
        else:
            appending_char = "<"
        code += appending_char * abs(new_bin - current_bin)
        if ord(char) - bins[new_bin] > 0:
            appending_char = "+"
        else:
            appending_char = "-"
        code += (appending_char * abs( ord(char) - bins[new_bin])) + "."
        current_bin = new_bin
        bins[new_bin] = ord(char)

    return code


def is_valid_bf(data: str) -> bool:
    for char in data:
        if char not in "><+-.,[]":
            return False

    return True


def decompress_if_necessary(data: str) -> str:
    if not is_valid_bf(data):
        data = bytes(base64.b64decode(data), "utf-8")
        data = zlib.decompress(data)
        if not is_valid_bf(data):
            raise ValueError("Data could not be resolved to Brainfuck code.")

    return data


def run_bf(data: str, stack_size: int) -> list:
    return nbfi.run(decompress_if_necessary(data))


# Gibberish Generator (Python).
# Algorithm: Letter-based Markov text generator.
# Original code written in JavaScript:
# Keith Enevoldsen, thinkzone.wlonk.com
# Ported to Python by garlicOS®
def _pick_match_index(text: str, target: str) -> int:
    N_CHARS = len(text)

    # Find all sets of matching target characters.
    n_matches = 0
    counter = -1
    while True:
        try:
            counter = text.index(target[counter + 1])
        except ValueError:
            break
        if counter >= N_CHARS:
            break
        else:
            n_matches += 1

    # Pick a match at random.
    return random.randint(0, n_matches)


def _pick_char(text: str, target: str, match_index: int, level: int) -> str:
    N_CHARS = len(text)

    # Find the character following the matching characters.
    n_matches = 0
    j = -1
    while True:
        try:
            j = text.index(target[j + 1])
        except ValueError:
            break
        if j >= N_CHARS:
            break
        elif match_index == n_matches:
            return text[j + level - 1]
        else:
            n_matches += 1


def generate_gibberish(text: str, level: int=4, length: int=500) -> str:
    N_CHARS = len(text)

    if N_CHARS < level:
        raise ValueError("Too few input characters.")

    char_index = None

    # Make the string contain two copies of the input text.
    # This allows for wrapping to the beginning when the end is reached.
    text += text

    # Ensure the input text ends with a space.
    if text[-1] != " ":
        text += " "

    # Pick a random starting character, preferably an uppercase letter.
    for _ in range(1000):
        char_index = random.randint(0, N_CHARS)
        if text[char_index].isupper():
            break

    # Write starting characters.
    output = text[char_index : char_index + level]

    # Set target string.
    target = text[char_index + 1 : char_index + level]

    # Generate characters.
    for _ in range(length):
        if (level == 1):
            # Pick a random character.
            output += text[random.randint(0, N_CHARS)]
        else:
            match_index = _pick_match_index(text, target)
            char = _pick_char(text, target, match_index, level)

            # Update the target.
            target = target[1 : level - 1] + char

            # Add the character to the output.
            output += char

    return output


def humanize_text(message: Message, text: str) -> str:
    for user in message.mentions:
        text = text.replace(user.mention, user.display_name)
    for channel in message.channel_mentions:
        text = text.replace(channel.mention, channel.name)
    for role in message.role_mentions:
        text = text.replace(role.mention, role.name)
    return text


naughty_words = requests.get("https://gist.github.com/ryanlewis/a37739d710ccdb4b406d/raw/0fbd315eb2900bb736609ea894b9bde8217b991a/google_twunter_lol")
naughty_words = "(" + naughty_words.text.replace("\r", "").replace("\n", ")|(") + ")"
naughty_words = re.compile(naughty_words, re.IGNORECASE)
def filter_naughty_words(text: str) -> str:
    return re.sub(naughty_words, "", text)
