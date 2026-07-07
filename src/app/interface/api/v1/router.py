from fastapi import APIRouter

from app.interface.api.controllers.example_controller import router as example_router
from app.interface.api.controllers.health_controller import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(example_router)
