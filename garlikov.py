import random
from typing import Literal, cast

import markovify


RESPONSE = "__RESPONSE__"
WILDCARD = "__WILDCARD__"

type WildcardState = tuple[str | Literal["__WILDCARD__"], ...]
type State = tuple[str, ...]


class Garlikov(markovify.Text):
	def __init__(self, parsed_sentences: list[list[str]]):
		super().__init__(None, parsed_sentences=parsed_sentences, state_size=3)
		self.compile(inplace=True)

	def respond(self, input_message: str) -> str:
		init_state = self.make_init_state(input_message)
		result = self.make_sentence(init_state=init_state, test_output=False)
		if result is None:
			return "Error"
		init_length = 0
		for token in init_state:
			init_length += len(token) + 1
		return result[init_length:]

	def resolve_wildcards(self, wild_state: WildcardState) -> State | None:
		"""
		Choose a state that is like the given state in all the part that aren't
		wildcards.
		"""
		states = self.chain.model.keys()
		# Filter the haystack of states down to just the ones that match all the
		# needle state's non-wild parts.
		for i, part in enumerate(wild_state):
			if part == WILDCARD:
				continue
			# Filter the haystack of states down to just the ones that match
			# this non-wild part of the wild state.
			states = [state for state in states if state[i] == part]
		if len(states) == 0:
			return None
		return random.choice(cast(list[State], states))

	def make_init_state(self, input_message: str) -> State:
		"""
		Settle for a state that is less-and-less similar from the one that comes
		from the input message, based on what is available in the model.
		"""
		first, last = encode_prompt(input_message)
		# Best case: the model knows this state exactly
		state = (first, last, RESPONSE)
		if state in self.chain.model:
			return state
		# Next best: model knows a state with just the first word
		state = self.resolve_wildcards((first, WILDCARD, RESPONSE))
		if state is not None:
			return state
		# Next best: just the last word
		state = self.resolve_wildcards((WILDCARD, last, RESPONSE))
		if state is not None:
			return state
		# Worst case: any state that starts the response
		state = self.resolve_wildcards((WILDCARD, WILDCARD, RESPONSE))
		assert state is not None, (
			"Corrupt: corpus does not contain the RESPONSE token"
		)
		return state


# string.punctuation sans the special characters Discord uses
PUNCTUATION = "!\"$%'()*+,-./;=?[\\]^_`{|}~"
punctuation_remover = str.maketrans("", "", PUNCTUATION)


def encode_word(word: str) -> str:
	return word.lower().translate(punctuation_remover)


def encode_prompt(text: str) -> tuple[str, str]:
	words = text.split()
	first = encode_word(words[0])
	last = encode_word(words[-1])
	return first, last
