from fastapi import APIRouter
from web.main_views import router as main_router
from web.short_url import router as short_url_router
from web.film import router as film_router

router = APIRouter()
router.include_router(main_router)
router.include_router(short_url_router)
router.include_router(film_router)
