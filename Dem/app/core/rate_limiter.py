import time
from collections import defaultdict
from typing import Callable, Tuple

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.response import error, ErrorCode


class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clients: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old entries
        cutoff = now - self.window_seconds
        self._clients[client_ip] = [t for t in self._clients[client_ip] if t > cutoff]

        if len(self._clients[client_ip]) >= self.max_requests:
            return Response(
                content=str(error(ErrorCode.RATE_LIMIT_EXCEEDED, "Too many requests, please try again later.")),
                status_code=429,
                media_type="application/json",
            )

        self._clients[client_ip].append(now)
        return await call_next(request)


def setup_rate_limiting(app, max_requests: int = 60, window_seconds: int = 60) -> None:
    app.add_middleware(SimpleRateLimitMiddleware, max_requests=max_requests, window_seconds=window_seconds)
