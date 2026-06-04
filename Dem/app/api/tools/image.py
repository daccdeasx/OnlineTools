from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import StreamingResponse
import io

from app.services.image_service import open_image, get_image_info, compress_image, resize_image, convert_image_format
from app.utils.file_utils import validate_file_size, validate_image_type
from app.utils.response import success, error, ErrorCode

router = APIRouter(prefix="/image", tags=["Image"])


def _mime_type(fmt: str) -> str:
    mt = fmt.lower()
    mapping = {"jpeg": "image/jpeg", "jpg": "image/jpeg", "png": "image/png", "webp": "image/webp", "gif": "image/gif"}
    return mapping.get(mt, "application/octet-stream")


@router.post("/info", response_model=dict)
async def get_image_info_endpoint(file: UploadFile = File(...)):
    if not file.content_type:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "Content-Type header is required")
    ok, msg = validate_image_type(file.content_type)
    if not ok:
        return error(ErrorCode.FILE_TYPE_NOT_ALLOWED, msg)
    contents = await file.read()
    ok, msg = validate_file_size(len(contents))
    if not ok:
        return error(ErrorCode.FILE_TOO_LARGE, msg)
    try:
        img = open_image(contents)
        info = get_image_info(img)
        info["file_size"] = len(contents)
        return success(info)
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"Failed to process image: {str(e)}")


@router.post("/compress", response_model=dict)
async def compress_image_endpoint(
    file: UploadFile = File(...),
    quality: int = Query(85, ge=1, le=100),
    output_format: str = Query("jpeg"),
    return_type: str = Query("file", pattern="^(file|json)$"),
):
    if not file.content_type:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "Content-Type header is required")
    ok, msg = validate_image_type(file.content_type)
    if not ok:
        return error(ErrorCode.FILE_TYPE_NOT_ALLOWED, msg)
    contents = await file.read()
    ok, msg = validate_file_size(len(contents))
    if not ok:
        return error(ErrorCode.FILE_TOO_LARGE, msg)
    try:
        img = open_image(contents)
        compressed = compress_image(img, quality=quality, output_format=output_format)
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"Failed to compress image: {str(e)}")

    if return_type == "json":
        return success({
            "original_size": len(contents),
            "compressed_size": len(compressed),
            "ratio": round(len(compressed) / len(contents), 4),
        })
    return StreamingResponse(
        io.BytesIO(compressed),
        media_type=_mime_type(output_format),
        headers={
            "X-Original-Size": str(len(contents)),
            "X-Compressed-Size": str(len(compressed)),
        },
    )


@router.post("/resize", response_model=dict)
async def resize_image_endpoint(
    file: UploadFile = File(...),
    width: int = Query(0, ge=0),
    height: int = Query(0, ge=0),
    keep_aspect_ratio: bool = True,
    return_type: str = Query("json", pattern="^(file|json)$"),
):
    if not file.content_type:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "Content-Type header is required")
    ok, msg = validate_image_type(file.content_type)
    if not ok:
        return error(ErrorCode.FILE_TYPE_NOT_ALLOWED, msg)
    contents = await file.read()
    ok, msg = validate_file_size(len(contents))
    if not ok:
        return error(ErrorCode.FILE_TOO_LARGE, msg)
    if width <= 0 and height <= 0:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "At least one of width or height must be positive")
    try:
        img = open_image(contents)
        resized = resize_image(img, width or None, height or None, keep_aspect_ratio)
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"Failed to resize image: {str(e)}")

    if return_type == "json":
        return success({
            "original": {"width": img.width, "height": img.height},
            "resized": {"width": resized.width, "height": resized.height},
        })

    buf = io.BytesIO()
    fmt = img.format or "PNG"
    if resized.mode not in ("RGB", "RGBA"):
        resized = resized.convert("RGB")
    resized.save(buf, format=fmt)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type=_mime_type(fmt),
        headers={
            "X-Original-Width": str(img.width),
            "X-Original-Height": str(img.height),
            "X-Resized-Width": str(resized.width),
            "X-Resized-Height": str(resized.height),
        },
    )


@router.post("/convert", response_model=dict)
async def convert_image_endpoint(
    file: UploadFile = File(...),
    target_format: str = Query("png"),
    return_type: str = Query("file", pattern="^(file|json)$"),
):
    if not file.content_type:
        return error(ErrorCode.PARAM_VALIDATION_FAILED, "Content-Type header is required")
    ok, msg = validate_image_type(file.content_type)
    if not ok:
        return error(ErrorCode.FILE_TYPE_NOT_ALLOWED, msg)
    contents = await file.read()
    ok, msg = validate_file_size(len(contents))
    if not ok:
        return error(ErrorCode.FILE_TOO_LARGE, msg)
    allowed_formats = {"png", "jpeg", "jpg", "webp", "gif"}
    if target_format.lower() not in allowed_formats:
        return error(ErrorCode.UNSUPPORTED_FORMAT, f"Target format must be one of: {', '.join(sorted(allowed_formats))}")
    try:
        img = open_image(contents)
        converted = convert_image_format(img, target_format)
    except Exception as e:
        return error(ErrorCode.SERVER_INTERNAL_ERROR, f"Failed to convert image: {str(e)}")

    if return_type == "json":
        return success({
            "original_format": img.format or "unknown",
            "target_format": target_format,
            "output_size": len(converted),
        })
    return StreamingResponse(
        io.BytesIO(converted),
        media_type=_mime_type(target_format),
        headers={"X-Original-Format": img.format or "unknown", "X-Target-Format": target_format},
    )

