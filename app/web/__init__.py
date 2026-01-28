from fastapi import APIRouter
from web.main_views import router as main_router
from web.short_url import router as short_url_router

router = APIRouter(
    include_in_schema=False,
)
router.include_router(main_router)
router.include_router(short_url_router)
