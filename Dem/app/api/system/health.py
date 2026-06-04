from fastapi import APIRouter

from app.utils.response import success

router = APIRouter(tags=["System"])


@router.get("/health", response_model=dict)
async def health_check():
    return success({"status": "healthy", "version": "0.1.0"})
