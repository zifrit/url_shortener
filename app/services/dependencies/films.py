import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from starlette import status

from schemas import Films
from storage.film.crud import FilmStorage

log = logging.getLogger(__name__)


def get_film_storage(request: Request) -> FilmStorage:
    return request.app.state.film_storage  # type: ignore[no-any-return]


GetFilmStorage = Annotated[FilmStorage, Depends(get_film_storage)]


def prefetch_film(
    slug: str,
    storage: GetFilmStorage,
) -> Films:

    if film := storage.get_by_slug(slug=slug):
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug} not found.",
    )


FilmBySlug = Annotated[
    Films,
    Depends(prefetch_film),
]
