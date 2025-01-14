"""
crimsoBOT image processing
https://github.com/crimsobot/crimsoBOT/blob/master/crimsobot/utils/image.py
MIT License
Copyright (c) 2019 crimso, williammck
"""

import asyncio
import functools
from collections.abc import Awaitable, Callable
from io import BytesIO
from typing import Concatenate, ParamSpec, TypeAlias, cast

import aiohttp
from PIL import Image, ImageSequence


MAX_FRAMES = 300
MAX_FILESIZE_BYTES = 10 * 1024 * 1024  # 10MB


P = ParamSpec("P")
# noqa: UP040 - ruff broken with `type` syntax + ParamSpecs as of v0.8.3
ImageProcessingFunction: TypeAlias = Callable[  # noqa: UP040
	Concatenate[Image.Image, P], Image.Image
]


def executor_function[**P, Ret](
	sync_function: Callable[P, Ret],
) -> Callable[P, Awaitable[Ret]]:
	@functools.wraps(sync_function)
	async def decorated(*args: P.args, **kwargs: P.kwargs) -> Ret:
		loop = asyncio.get_event_loop()
		reconstructed_function = functools.partial(
			sync_function, *args, **kwargs
		)
		return await loop.run_in_executor(None, reconstructed_function)

	return decorated


def gif_frame_transparency(img: Image.Image) -> Image.Image:
	# get alpha mask
	alpha = img.convert("RGBA").split()[-1]
	# convert back to P mode but only using 255 of available 256 colors
	img = img.convert("RGB").convert(
		"P", palette=Image.Palette.ADAPTIVE, colors=255
	)
	# set all pixel values in alpha below threshhold to 255 and the rest to 0
	mask = Image.eval(alpha, lambda a: 255 if a <= 88 else 0)
	# paste the color of index 255 and use alpha as a mask
	img.paste(255, mask)  # the transparency index will later be set to 255
	return img


def image_to_buffer(
	image_list: list[Image.Image],
	durations: tuple[int, ...] | None = None,
	it_loops: bool | None = None,
) -> BytesIO:
	buffer = BytesIO()

	if not durations:  # equiv. to `durations is None or len(durations) == 0`
		image_list[0].save(buffer, "WEBP")
	else:
		giffed_frames: list[Image.Image] = []
		for frame in image_list:
			new_frame = gif_frame_transparency(frame)
			giffed_frames.append(new_frame)
		if it_loops:
			giffed_frames[0].save(
				buffer,
				format="GIF",
				transparency=255,
				append_images=giffed_frames[1:],
				save_all=True,
				duration=durations,
				loop=0,
				disposal=2,
			)
		else:
			giffed_frames[0].save(
				buffer,
				format="GIF",
				transparency=255,
				append_images=giffed_frames[1:],
				save_all=True,
				duration=durations,
				disposal=2,
			)
	buffer.seek(0)
	return buffer


async def fetch_image(url: str) -> Image.Image:
	"""Determine type of input, return image file."""
	async with aiohttp.ClientSession() as session:
		async with session.get(url, allow_redirects=False) as response:
			img_bytes = await response.read()
			if len(img_bytes) > MAX_FILESIZE_BYTES:
				raise Exception("too big")
			return Image.open(BytesIO(img_bytes))


def resize_img(img: Image.Image, scale: float) -> Image.Image:
	width, height = img.size
	return img.resize(
		(int(width * scale), int(height * scale)),
		resample=Image.Resampling.LANCZOS,
	)


@executor_function
def process_lower_level(
	img: Image.Image,
	effect: ImageProcessingFunction[P],
	*args: P.args,
	**kwargs: P.kwargs,
) -> BytesIO:
	# this will only loop once for still images
	frames: list[Image.Image] = []
	durations: list[int] = []

	# if a GIF loops, it will have the attribute loop = 0; if not, then
	# attribute does not exist
	image_loop = getattr(img.info, "loop", False)

	for _ in ImageSequence.Iterator(img):
		if image_loop:
			duration: int = img.info["duration"]
			durations.append(duration)
		img_out = effect(img.convert("RGBA"), *args, **kwargs)
		frames.append(img_out)

	buffer = image_to_buffer(frames, tuple(durations), image_loop)
	return buffer


async def process(
	image_url: str,
	effect: ImageProcessingFunction[P],
	*args: P.args,
	**kwargs: P.kwargs,
) -> BytesIO:
	img = await fetch_image(image_url)
	is_gif = getattr(img, "is_animated", False)

	if is_gif:
		n_frames = cast(int, getattr(img, "n_frames"))
		if n_frames > MAX_FRAMES:
			raise NotImplementedError(
				"GIF too long; need to process only first frame"
			)

	# if we have to resize, try to do so before processing to preserve quality
	n_bytes = img.size[0] * img.size[1]
	buffer = None
	while n_bytes > MAX_FILESIZE_BYTES:
		if buffer is not None:
			img = Image.open(buffer)
		scale = 0.9 * MAX_FILESIZE_BYTES / n_bytes
		buffer = await process_lower_level(img, resize_img, scale)
		n_bytes = buffer.getbuffer().nbytes
	if buffer is not None:
		img = Image.open(buffer)

	# original image begins processing
	buffer = await process_lower_level(img, effect, *args, **kwargs)
	n_bytes = buffer.getbuffer().nbytes

	# if file too large to send via Discord, then resize
	while n_bytes > MAX_FILESIZE_BYTES:
		# recursively resize image until it meets Discord filesize limit
		img = Image.open(buffer)
		# 0.9x bias to help ensure it comes in under max size
		scale = 0.9 * MAX_FILESIZE_BYTES / n_bytes
		buffer = await process_lower_level(img, resize_img, scale)
		n_bytes = buffer.getbuffer().nbytes

	return buffer
