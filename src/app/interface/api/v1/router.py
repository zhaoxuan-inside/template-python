from fastapi import APIRouter

from app.interface.api.v1.example.example_controller import router as example_router
from app.interface.api.v1.health.health_controller import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(example_router)
