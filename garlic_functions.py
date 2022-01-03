import random
import base64
import zlib
import nbfi
from discord import Message
from utils import chance


def generate_scream() -> str:
    # Vanilla scream half the time
    if chance(50):
        return "A" * random.randint(1, 100)

    # One of these choices repeated 1-100 times
    body = random.choice(["A", "O"]) * random.randint(1, 100)

    # Chance to wrap the message in one of these Markdown strings
    formatter = "" if chance(50) else random.choice(["*", "**", "***"])

    # Chance to put one of these at the end of the message
    suffix = "" if chance(50) else random.choice(["H", "RGH","GH""CGH"])

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
def __execute(code: list, stack_size: int) -> list:
    """Run BF code"""
    iptr = 0
    sptr = 0
    output = ""
    stack = list(0 for _ in range(stack_size))
    code_len = len(code)

    while iptr < code_len:
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


def string_to_bf(source_string):
    """
    Convert a string into a BF program. Returns the BF code.
    Thank you to yiangos on GitHub
    """
    num_glyphs = len(source_string)
    number_of_bins = max(max([ord(c) for c in source_string]) // num_glyphs, 1)
    bins = [(i + 1) * number_of_bins for i in range(num_glyphs)]
    code = "+" * number_of_bins + "["
    code += "".join([">" + ("+" * (i + 1)) for i in range(1, num_glyphs)])
    code += "<" * (num_glyphs - 1) + "-]"
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
        code += (appending_char * abs(ord(char) - bins[new_bin])) + "."
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


def run_bf(data: str) -> list:
    return nbfi.run(decompress_if_necessary(data))


def humanize_text(message: Message, text: str) -> str:
    for user in message.mentions:
        text = text.replace(user.mention, user.display_name)
    for channel in message.channel_mentions:
        text = text.replace(channel.mention, channel.name)
    for role in message.role_mentions:
        text = text.replace(role.mention, role.name)
    return text
