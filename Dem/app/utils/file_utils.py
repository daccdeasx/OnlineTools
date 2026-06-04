import os
import tempfile
from pathlib import Path
from typing import Tuple

MAX_UPLOAD_SIZE = 10 * 1024 * 1024

ALLOWED_IMAGE_TYPES = frozenset({
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
})


def validate_file_size(size: int, max_bytes: int = MAX_UPLOAD_SIZE) -> Tuple[bool, str]:
    if size > max_bytes:
        return False, f"File exceeds maximum size of {max_bytes // (1024 * 1024)} MB"
    return True, ""


def validate_image_type(content_type: str) -> Tuple[bool, str]:
    if content_type not in ALLOWED_IMAGE_TYPES:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_TYPES))
        return False, f"Unsupported image type '{content_type}'. Allowed: {allowed}"
    return True, ""


def save_temp_file(contents: bytes, suffix: str = "") -> Path:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    path_obj = Path(path)
    path_obj.write_bytes(contents)
    return path_obj


def remove_temp_file(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except OSError:
        pass
