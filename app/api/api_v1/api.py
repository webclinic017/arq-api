from fastapi import APIRouter

from.endpoints import models

router = APIRouter()
router.include_router(models.router, prefix="/models", tags=["models"])