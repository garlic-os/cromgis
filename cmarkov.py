from typing import Protocol

from convmark import ConvMark

import badmarkov


__all__ = ["CromgisMarkov", "AwfulMarkov", "ConvMark"]


class CromgisMarkov(Protocol):
	def respond(self, input_message: str) -> str: ...


class AwfulMarkov(badmarkov.AwfulMarkov):
	def respond(self, input_message: str) -> str:
		return self.generate()
