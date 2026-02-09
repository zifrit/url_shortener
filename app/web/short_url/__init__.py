from fastapi import APIRouter

from web.short_url.details import router as details_router
from web.short_url.updated import router as update_router
from web.short_url.list import router as list_router

router = APIRouter(
    prefix="/short-urls",
    tags=["short-urls"],
)
router.include_router(list_router)
router.include_router(details_router)
router.include_router(update_router)
