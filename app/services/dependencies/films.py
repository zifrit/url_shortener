import logging
from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from core import config
from storage.film.crud import FilmStorage
from schemas import Films

log = logging.getLogger(__name__)


def get_film_storage() -> FilmStorage:
    return FilmStorage(hash_name=config.settings.redis.token.film)


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
