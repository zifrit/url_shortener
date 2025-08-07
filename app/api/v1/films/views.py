from typing import Annotated

from fastapi import APIRouter, Depends

from api.v1.films.crud import FILMS
from schemas import Films
from services.dependencies.films import prefetch_film

router = APIRouter(prefix="/films")


@router.get("/films/", response_model=list[Films])
def read_film_list() -> list[Films]:
    return FILMS


@router.get("/films/{film_id}/", response_model=Films)
def read_film_list(film: Annotated[Films, Depends(prefetch_film)]) -> Films:
    return film
