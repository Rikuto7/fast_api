from fastapi import APIRouter
from app.api.routers.test import router as test_router


router = APIRouter()
router.include_router(test_router, prefix="/test", tags=["test"])