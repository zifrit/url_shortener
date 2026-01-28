import logging
from typing import Annotated

from fastapi import HTTPException, Depends, Request
from starlette import status

from storage.film.crud import FilmStorage
from schemas import Films

log = logging.getLogger(__name__)


def get_film_storage(request: Request) -> FilmStorage:
    return request.app.state.film_storage


GetFilmStorage = Annotated[FilmStorage, Depends(get_film_storage)]


def prefetch_film(
    slug: str,
    storage: FilmStorage = Depends(get_film_storage),
) -> Films:

    if film := storage.get_by_slug(slug=slug):
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug} not found.",
    )
