from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING

import matplotlib.image as plt
import numpy as np
from PIL import Image

import crimage


if TYPE_CHECKING:
	import numpy.typing as npt


MAX_FRAMES = 300
MAX_FILESIZE_BYTES = 10 / 1024 * 1024  # 10MB

# Determine color group using strict thresholds
# Adjust this value to make grouping more/less strict
TRESHOLD_COLOR_GROUP = 1.2


class ColorGroup(Enum):
	GRAYSCALE = np.uint8(0)
	RED = np.uint8(1)
	GREEN = np.uint8(2)
	BLUE = np.uint8(3)
	YELLOW = np.uint8(4)
	MAGENTA = np.uint8(5)
	CYAN = np.uint8(6)
	MIXED = np.uint8(7)


def sort_pixels_by_color(img: Image.Image) -> Image.Image:
	"""
	solst-ice/pxl-srt Python+PIL port
	https://github.com/solst-ice/pxl-srt/commit/5e82ae6/src/utils/imageProcessing.js
	"""
	# 2D array of image's pixels as received from this function crimsoBOT uses
	# shape: (..., ..., 4)
	raster: npt.NDArray[np.uint8] = plt.pil_to_array(img)
	# assert len(raster.shape) == 3
	# assert raster.shape[2] == 4

	# 1D array of raster's pixels + extra information per pixel. So pixels can
	# be sorted as a 1D array
	# shape: (..., 6)
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
			pixel: tuple[np.uint8, np.uint8, np.uint8, np.uint8] = raster[i, j]
			r, g, b, a = pixel

			# Calculate luminosity
			luminosity = (np.uint16(r) + g + b) / 3

			if (
				abs(np.int16(r) - g) < 10
				and abs(np.int16(g) - b) < 10
				and abs(np.int16(r) - b) < 10
			):
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

			pixels[i * raster.shape[1] + j][0] = r
			pixels[i * raster.shape[1] + j][1] = g
			pixels[i * raster.shape[1] + j][2] = b
			pixels[i * raster.shape[1] + j][3] = a
			pixels[i * raster.shape[1] + j][4] = color_group.value
			pixels[i * raster.shape[1] + j][5] = luminosity

	# Sort the pixels
	indices = np.lexsort((pixels["color_group"], pixels["luminosity"]))
	sorted_pixels = pixels[indices]

	# Put sorted pixels back into the raster
	# throw away the old raster, create a new one that we can write to
	raster = np.ndarray(shape=raster.shape, dtype=np.uint8)
	for i in range(raster.shape[0]):
		for j in range(raster.shape[1]):
			for k in range(4):
				raster[i, j, k] = sorted_pixels[i * raster.shape[1] + j][k]

	sorted_raster_fp = BytesIO()
	plt.imsave(sorted_raster_fp, raster)
	sorted_raster_fp.seek(0)
	return Image.open(sorted_raster_fp)


async def pxl_srt(image_url: str) -> BytesIO:
	return await crimage.process(image_url, sort_pixels_by_color)
