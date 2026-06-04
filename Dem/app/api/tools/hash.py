from fastapi import APIRouter, Body
from pydantic import BaseModel, Field

from app.services.hash_service import compute_hash_from_text, is_supported_algorithm
from app.utils.response import success, error, ErrorCode

router = APIRouter(prefix="/hash", tags=["Hash"])


class HashRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1_000_000, description="Text to hash")
    algorithm: str = Field(
        default="sha256",
        pattern=r"^(md5|sha1|sha256|sha384|sha512)$",
        description="Hash algorithm",
    )


class HashResponse(BaseModel):
    algorithm: str
    hash: str


@router.post("/compute", response_model=dict)
async def compute_hash(req: HashRequest):
    algo = req.algorithm.lower()
    if not is_supported_algorithm(algo):
        return error(ErrorCode.PARAM_VALIDATION_FAILED, f"Unsupported algorithm: {req.algorithm}")

    result = compute_hash_from_text(req.text, algo)
    return success({"algorithm": algo, "hash": result})
