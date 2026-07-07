from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.infrastructure.database.core import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def health_check(db: Annotated[AsyncSession, Depends(get_db)]):
    return {"status": "ok", "service": settings.app_name, "version": "1.0.0"}
