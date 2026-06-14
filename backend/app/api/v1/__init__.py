from fastapi import APIRouter
from app.api.v1 import health, ping

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(ping.router)
# Сюда backend-разработчик добавит:
# router.include_router(auth.router)
# router.include_router(regions.router)
# ...