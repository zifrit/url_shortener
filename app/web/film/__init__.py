from fastapi import APIRouter

from web.film.details import router as details_router
from web.film.list import router as film_router

router = APIRouter(
    prefix="/film",
    tags=["film"],
)
router.include_router(film_router)
router.include_router(details_router)
