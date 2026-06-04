import time
from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None
    timestamp: int = 0

    model_config = {"extra": "forbid"}


def success(data: Any = None, message: str = "success") -> dict:
    return {
        "code": 0,
        "message": message,
        "data": data,
        "timestamp": int(time.time()),
    }


def error(code: int, message: str, data: Any = None) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": int(time.time()),
    }


class ErrorCode:
    SUCCESS = 0
    PARAM_VALIDATION_FAILED = 1001
    UNSUPPORTED_FORMAT = 1002
    FILE_TOO_LARGE = 2001
    FILE_TYPE_NOT_ALLOWED = 2002
    RATE_LIMIT_EXCEEDED = 429
    SERVER_INTERNAL_ERROR = 5000
