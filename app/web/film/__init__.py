from fastapi import APIRouter
from web.film.list import router as film_router

router = APIRouter(
    prefix="/film",
)
router.include_router(film_router)
