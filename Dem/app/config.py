import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "OnlineTools"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 2

    # CORS
    cors_origins: List[str] = ["*"]

    # Rate limiting (per-IP)
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 60
    rate_limit_window: int = 60  # seconds

    # File upload
    max_upload_size_mb: int = 10
    allowed_image_types: List[str] = [
        "image/png",
        "image/jpeg",
        "image/webp",
        "image/gif",
    ]

    # JWT (reserved for future user system)
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # Redis (optional)
    redis_url: str = "redis://localhost:6379/0"

    # CSP
    csp_enabled: bool = True

    model_config = {
        "env_prefix": "OT_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
