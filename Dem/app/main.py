from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.config import get_settings
from app.core.security import setup_security
from app.core.exceptions import setup_exception_handlers
from app.core.rate_limiter import setup_rate_limiting


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="OnlineTools - Lightweight online utility toolbox API",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    setup_security(app)
    setup_exception_handlers(app)

    if settings.rate_limit_enabled:
        setup_rate_limiting(
            app,
            max_requests=settings.rate_limit_requests,
            window_seconds=settings.rate_limit_window,
        )

    app.include_router(api_router)

    return app


app = create_app()
