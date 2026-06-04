import io
from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image


MAX_WIDTH = 4096
MAX_HEIGHT = 4096


def open_image(source: Union[Path, bytes]) -> Image.Image:
    if isinstance(source, Path):
        return Image.open(source)
    return Image.open(io.BytesIO(source))


def get_image_info(image: Image.Image) -> dict:
    return {
        "width": image.width,
        "height": image.height,
        "format": image.format or "UNKNOWN",
        "mode": image.mode,
    }


def resize_image(
    image: Image.Image,
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True,
) -> Image.Image:
    if width is None and height is None:
        return image.copy()

    orig_width, orig_height = image.width, image.height

    if keep_aspect_ratio:
        if width is None:
            ratio = height / orig_height
            width = int(orig_width * ratio)
        elif height is None:
            ratio = width / orig_width
            height = int(orig_height * ratio)
        else:
            ratio = min(width / orig_width, height / orig_height)
            width = int(orig_width * ratio)
            height = int(orig_height * ratio)

    width = min(width, MAX_WIDTH)
    height = min(height, MAX_HEIGHT)

    return image.resize((width, height), Image.LANCZOS)


def compress_image(
    image: Image.Image,
    quality: int = 85,
    output_format: str = "JPEG",
) -> bytes:
    buf = io.BytesIO()

    save_format = output_format.upper()
    if save_format == "JPG":
        save_format = "JPEG"

    save_kwargs = {}
    if save_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality
        save_kwargs["optimize"] = True
    elif save_format == "PNG":
        save_kwargs["optimize"] = True

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    image.save(buf, format=save_format, **save_kwargs)
    return buf.getvalue()


def convert_image_format(image: Image.Image, target_format: str) -> bytes:
    buf = io.BytesIO()

    fmt = target_format.upper()
    if fmt == "JPG":
        fmt = "JPEG"

    image.save(buf, format=fmt)
    return buf.getvalue()
