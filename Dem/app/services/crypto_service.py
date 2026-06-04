import base64
import hashlib
import secrets
from typing import Tuple

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def generate_aes_key(bits: int = 256) -> bytes:
    return secrets.token_bytes(bits // 8)


def generate_aes_iv() -> bytes:
    return secrets.token_bytes(16)


def aes_encrypt(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
    iv = generate_aes_iv()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext, iv


def aes_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    return plaintext


def base64_encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def base64_decode(encoded: str) -> bytes:
    return base64.b64decode(encoded.encode("utf-8"))


def md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
