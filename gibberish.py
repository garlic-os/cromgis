# Gibberish Generator (JavaScript).
# Algorithm: Letter-based Markov text generator.
# Keith Enevoldsen, thinkzone.wlonk.com

import random
import math

def _char_at(text: str, index: int) -> str:
    try:
        return text[index]
    except IndexError:
        return ""


def _index_of(text: str, substring: str, start: str=None, end: str=None) -> int:
    try:
        return text.index(substring, start, end)
    except ValueError:
        return -1


def generate_gibberish(text: str, lev: int) -> str:
    nchars = len(text)

    # Make the string contain two copies of the input text.
    # This allows for wrapping to the beginning when the end is reached.
    text = text + text

    ichar = None
    char = None
    nmatches = None
    j = None
    imatch = None

    # Check input length.
    if nchars < lev:
        print("Too few input characters.")
        return

    # Pick a random starting character, preferably an uppercase letter.
    for i in range(1000):
        ichar = math.floor(nchars * random.random())
        char = _char_at(text, ichar)
        if char.isupper():
            break

    # Write starting characters.
    output = text[ichar:ichar + lev]

    # Set target string.
    target = text[ichar + 1:ichar + lev]

    # Generate characters.
    for i in range(500):
        if lev == 1:
            # Pick a random character.
            char = _char_at(text, math.floor(nchars * random.random()))
        else:
            # Find all sets of matching target characters.
            nmatches = 0
            j = -1
            while True:
                j = _index_of(text, target, j + 1)
                if j < 0 or j >= nchars:
                    break
                else:
                    nmatches += 1

            # Pick a match at random.
            imatch = math.floor(nmatches * random.random())

            nmatches = 0
            j = -1
            while True:
                j = _index_of(text, target, j + 1)
                if j < 0 or j >= nchars:
                    raise Exception("This should not happen")
                elif imatch == nmatches:
                    char = _char_at(text, j + lev - 1)
                else:
                    nmatches += 1

        # Output the character.
        output += char

        # Update the target.
        if lev > 1:
            target = target[1:lev - 1] + char

    return output
