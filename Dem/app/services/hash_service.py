import hashlib
from typing import Optional


# Supported hash algorithms matching the architecture spec
SUPPORTED_ALGORITHMS = frozenset({"md5", "sha1", "sha256", "sha384", "sha512"})


def compute_hash(data: bytes, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def compute_hash_from_text(text: str, algorithm: str) -> str:
    data = text.encode("utf-8")
    return compute_hash(data, algorithm)


def is_supported_algorithm(algorithm: str) -> bool:
    return algorithm.lower() in SUPPORTED_ALGORITHMS
