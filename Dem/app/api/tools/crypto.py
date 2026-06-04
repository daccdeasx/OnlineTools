import base64

from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from app.services.crypto_service import (
    aes_encrypt,
    aes_decrypt,
    generate_aes_key,
    generate_aes_iv,
)
from app.utils.response import success, error, ErrorCode

router = APIRouter(prefix="/crypto", tags=["Crypto"])


class AESEncryptRequest(BaseModel):
    plaintext: str = Field(..., min_length=1, max_length=1_000_000)
    key: str = Field(..., description="Base64-encoded AES key")


class AESDecryptRequest(BaseModel):
    ciphertext: str = Field(..., description="Base64-encoded ciphertext")
    key: str = Field(..., description="Base64-encoded AES key")
    iv: str = Field(..., description="Base64-encoded IV")


class AESKeyResponse(BaseModel):
    key: str
    iv: str


@router.post("/aes/generate-key", response_model=dict)
async def generate_key():
    key = generate_aes_key(256)
    iv = generate_aes_iv()
    return success({
        "key": base64.b64encode(key).decode("utf-8"),
        "iv": base64.b64encode(iv).decode("utf-8"),
    })


@router.post("/aes/encrypt", response_model=dict)
async def aes_encrypt_endpoint(req: AESEncryptRequest):
    try:
        key = base64.b64decode(req.key.encode("utf-8"))
        plaintext_bytes = req.plaintext.encode("utf-8")
    except Exception:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "Invalid Base64 key")

    try:
        ciphertext, iv = aes_encrypt(plaintext_bytes, key)
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"Encryption failed: {str(e)}")

    return success({
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "iv": base64.b64encode(iv).decode("utf-8"),
    })


@router.post("/aes/decrypt", response_model=dict)
async def aes_decrypt_endpoint(req: AESDecryptRequest):
    try:
        key = base64.b64decode(req.key.encode("utf-8"))
        iv = base64.b64decode(req.iv.encode("utf-8"))
        ciphertext_bytes = base64.b64decode(req.ciphertext.encode("utf-8"))
    except Exception:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "Invalid Base64 input")

    try:
        plaintext = aes_decrypt(ciphertext_bytes, key, iv)
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"Decryption failed: {str(e)}")

    return success({"plaintext": plaintext.decode("utf-8")})
