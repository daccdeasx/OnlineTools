import io

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.qr_service import generate_qr
from app.utils.response import success, error, ErrorCode

router = APIRouter(prefix="/qr", tags=["QR"])


class QRRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=3000, description="QR code content")
    size: int = Field(default=300, ge=100, le=600, description="Image size in pixels")


@router.post("/generate", response_model=dict)
async def generate_qr_code(req: QRRequest):
    try:
        png_bytes = generate_qr(req.text, size=req.size)
        return StreamingResponse(
            io.BytesIO(png_bytes),
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=qrcode.png",
                "X-QR-Size": str(req.size),
            },
        )
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"QR generation failed: {str(e)}")
