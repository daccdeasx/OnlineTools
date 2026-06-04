from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.charset_service import convert_encoding, get_supported_encodings
from app.utils.response import success, error, ErrorCode

router = APIRouter(prefix="/charset", tags=["Charset"])


class CharsetConvertRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000_000)
    from_encoding: str = Field(default="gbk")
    to_encoding: str = Field(default="utf-8")


@router.get("/encodings", response_model=dict)
async def list_encodings():
    return success({"encodings": get_supported_encodings()})


@router.post("/convert", response_model=dict)
async def convert_charset(req: CharsetConvertRequest):
    result, err = convert_encoding(req.text, req.from_encoding, req.to_encoding)
    if err:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, err)
    return success({
        "result": result,
        "from": req.from_encoding,
        "to": req.to_encoding,
    })
