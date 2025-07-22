from fastapi import APIRouter
from .hello import router as hello

router = APIRouter(prefix="/api/v1")
router.include_router(hello)
