import random
import string

import discord


class Crombed(discord.Embed):
	"""
	A Discord Embed with extra features!
	Concepts stolen from crimsoBOT; copyright (c) 2019 crimso, williammck; MIT
	https://github.com/crimsobot/crimsoBOT/blob/master/crimsobot/utils/tools.py
	"""

	colors = {
		"flesh": 0x98784C,
		"red": 0xD32F2F,
		"squid": 0xBEF4C3,
		"teal": 0x1EC9A1,
	}

	def __init__(self, **kwargs):
		if self.color is None:
			color_name = kwargs.get("color_name", "flesh")
			kwargs["color"] = Crombed.colors[color_name]
			kwargs.pop("color_name", None)
		super().__init__(**kwargs)


def chance(percent: float) -> bool:
	"""Random outcome with a <percent>% chance of being True."""
	return random.random() < percent / 100


def is_mention(text: str) -> bool:
	"""Determine if a string is a user mention."""
	correct_beginning = text[:2] == "<@"
	not_emoji = ":" not in text
	not_channel = "#" not in text
	correct_ending = text[-1] == ">"
	return correct_beginning and not_emoji and not_channel and correct_ending


def extract_id(text: str) -> int:
	"""Get a Discord ID from a string."""
	# Note: this is quite possibly the worst way to do this
	output = ""
	for char in text:
		if char in string.digits:
			output += char
	return int(output)


def random_string(length: int = 32) -> str:
	"""Generate a string of random letters and numbers."""
	""" Pasted from https://pythontips.com/2013/07/28/generating-a-random-string/ """
	return "".join(
		[
			random.choice(string.ascii_letters + string.digits)
			for _ in range(length)
		]
	)
