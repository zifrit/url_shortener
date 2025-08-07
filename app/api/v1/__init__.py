from fastapi import APIRouter
from .url_shortener.views import router as url_shortener_router
from .redirect import router as redirect_url_router
from .films.views import router as films_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(url_shortener_router, tags=["url_shortener"])
router.include_router(redirect_url_router, tags=["redirect_url"])
router.include_router(films_router, tags=["films"])
