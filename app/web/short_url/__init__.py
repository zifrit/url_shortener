from fastapi import APIRouter
from web.short_url.list import router as list_router

router = APIRouter(
    prefix="/short-urls",
)
router.include_router(list_router)
