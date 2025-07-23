from fastapi import APIRouter
from .hello import router as hello
from .notes import router as notes

router = APIRouter(prefix="/api/v1")
router.include_router(hello)
router.include_router(notes)
