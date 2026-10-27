from fastapi import APIRouter

from .card import router as card_router
from .user import router as user_router

router = APIRouter(prefix="/v1",)

router.include_router(card_router)
router.include_router(user_router)
