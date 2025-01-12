from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import Concatenate, ParamSpec, TypeAlias, cast

import matplotlib.image as plt
import numpy as np
from PIL import Image

from . import crimage


MAX_FRAMES = 300
MAX_FILESIZE_BYTES = 10 / 1024 * 1024  # 10MB


P = ParamSpec("P")
# noqa: UP040 - ruff broken with `type` syntax + ParamSpecs as of v0.8.3
ImageProcessingFunction: TypeAlias = Callable[  # noqa: UP040
	Concatenate[Image.Image, P], Image.Image
]


def rbg_to_hsl(r: float, g: float, b: float) -> tuple[float, float, float]:
	r /= 255
	g /= 255
	b /= 255

	channel_max = max(r, g, b)
	channel_min = min(r, g, b)
	l = (channel_max + channel_min) / 2

	if channel_max == channel_min:
		h = s = 0  # achromatic
	else:
		d = channel_max - channel_min
		if l > 0.5:
			s = d / (2 - channel_max - channel_min)
		else:
			s = d / (channel_max + channel_min)
		if channel_max == r:
			h = (g - b) / d + (6 if g < b else 0)
		elif channel_max == g:
			h = (b - r) / d + 2
		else:  # channel_max == b
			h = (r - g) / d + 4
		h /= 6

	return h * 360, s * 100, l * 100


class ColorGroup(Enum):
	GRAYSCALE = np.uint8(0)
	RED = np.uint8(1)
	GREEN = np.uint8(2)
	BLUE = np.uint8(3)
	YELLOW = np.uint8(4)
	MAGENTA = np.uint8(5)
	CYAN = np.uint8(6)
	MIXED = np.uint8(7)


@dataclass
class Pixel:
	r: np.uint8
	g: np.uint8
	b: np.uint8
	a: np.uint8
	color_group: ColorGroup
	luminosity: np.uint8

	# @property
	# def key(self) -> np.uint16:
	# 	"""Sort by color group, then luminosity.

	# 	Accomplished by packing color group and luminosity (both 8 bits each)
	# 	into a single (16-bit) number, where color group occupies the more
	# 	significant 8 bits.
	# 	"""
	# 	color_group_16 = np.uint16(self.color_group.value)
	# 	# no idea why Pylance thinks these are signedinteger[Any]
	# 	group_shifted = cast(np.uint16, color_group_16 << 8)
	# 	result = cast(np.uint16, group_shifted | self.luminosity)
	# 	return result

	# def __lt__(self, other: "Pixel"):
	# 	return self.key < other.key


# below are the blocking image functions (that support GIF) which require the
# executor_function wrapper

# Determine color group using strict thresholds
# Adjust this value to make grouping more/less strict
TRESHOLD_COLOR_GROUP = 1.2


def sort_pixels_by_color(img: Image.Image) -> Image.Image:
	"""
	solst-ice/pxl-srt Python port
	https://github.com/solst-ice/pxl-srt/commit/5e82ae6/src/utils/imageProcessing.js
	"""
	# raster: NDArray[np.uint8] = plt.pil_to_array(img)
	raster: np.ndarray[tuple[int, int, int], np.dtype[np.uint8]] = (
		plt.pil_to_array(img)
	)
	# assert len(raster.shape) == 3
	# assert raster.shape[2] == 4

	pixels = np.ndarray(
		(raster.shape[0] * raster.shape[1]),
		dtype=[
			("r", np.uint8),
			("g", np.uint8),
			("b", np.uint8),
			("a", np.uint8),
			("color_group", np.uint8),
			("luminosity", np.uint8),
		],
	)

	# Convert pixels to array of objects with color information
	for i in range(raster.shape[0]):
		for j in range(raster.shape[1]):
			r, g, b, a = raster[i, j]
			# Calculate luminosity
			luminosity = (r + g + b) / 3

			if abs(r - g) < 10 and abs(g - b) < 10 and abs(r - b) < 10:
				color_group = ColorGroup.GRAYSCALE
			elif r > g * TRESHOLD_COLOR_GROUP and r > b * TRESHOLD_COLOR_GROUP:
				color_group = ColorGroup.RED
			elif g > r * TRESHOLD_COLOR_GROUP and g > b * TRESHOLD_COLOR_GROUP:
				color_group = ColorGroup.GREEN
			elif b > r * TRESHOLD_COLOR_GROUP and b > g * TRESHOLD_COLOR_GROUP:
				color_group = ColorGroup.BLUE
			elif r > b and g > b:
				color_group = ColorGroup.YELLOW
			elif r > g and b > g:
				color_group = ColorGroup.MAGENTA
			elif g > r and b > r:
				color_group = ColorGroup.CYAN
			else:
				color_group = ColorGroup.MIXED

			pixels[i * raster.shape[0] + j, 0] = r
			pixels[i * raster.shape[0] + j, 1] = g
			pixels[i * raster.shape[0] + j, 2] = b
			pixels[i * raster.shape[0] + j, 3] = a
			pixels[i * raster.shape[0] + j, 4] = color_group
			pixels[i * raster.shape[0] + j, 5] = luminosity

	# Sort the pixels
	indices = np.lexsort((pixels["color_group"], pixels["luminosity"]))
	sorted_pixels = pixels[indices]

	# Put sorted pixels back into the raster
	for i in range(raster.shape[0]):
		for j in range(raster.shape[1]):
			for k in range(4):
				raster[i, j, k] = sorted_pixels[i * raster.shape[0] + j, k]

	sorted_raster_fp = BytesIO()
	plt.imsave(sorted_raster_fp, raster)
	sorted_raster_fp.seek(0)
	return Image.open(sorted_raster_fp)


async def pxl_srt(image_url: str) -> BytesIO:
	return await crimage.process(image_url, sort_pixels_by_color)
