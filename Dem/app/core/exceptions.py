from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.utils.response import error, ErrorCode


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=error(ErrorCode.PARAM_VALIDATION_FAILED, str(exc)),
    )


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content=error(ErrorCode.RATE_LIMIT_EXCEEDED, "Too many requests, please try again later."),
    )


async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error(ErrorCode.SERVER_INTERNAL_ERROR, "Internal server error."),
    )


def setup_exception_handlers(app) -> None:
    from fastapi.exceptions import RequestValidationError

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_exception_handler(Exception, internal_exception_handler)
