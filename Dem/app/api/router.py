from fastapi import APIRouter

from app.api.system.health import router as health_router
from app.api.system.stats import router as stats_router
from app.api.tools.hash import router as hash_router
from app.api.tools.crypto import router as crypto_router
from app.api.tools.image import router as image_router
from app.api.tools.qr import router as qr_router
from app.api.tools.charset import router as charset_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router, prefix="/system")
api_router.include_router(stats_router, prefix="/system")
api_router.include_router(hash_router, prefix="/tools")
api_router.include_router(crypto_router, prefix="/tools")
api_router.include_router(image_router, prefix="/tools")
api_router.include_router(qr_router, prefix="/tools")
api_router.include_router(charset_router, prefix="/tools")
