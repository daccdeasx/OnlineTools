from fastapi import APIRouter

from app.utils.response import success

router = APIRouter(tags=["System"])


@router.get("/ping", response_model=dict)
async def ping():
    return success("pong")
