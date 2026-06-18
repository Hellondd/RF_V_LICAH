from fastapi import APIRouter
from app.api.v1 import (
    health,
    ping,
    auth,
    regions,
    persons,
    achievements,
    quiz,
    postcards,
    admin,
    upload,
)

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(ping.router)
router.include_router(auth.router)
router.include_router(regions.router)
router.include_router(persons.router)
router.include_router(achievements.router)
router.include_router(quiz.router)
router.include_router(postcards.router)
router.include_router(admin.router)
router.include_router(upload.router)
