import logging

from fastapi import HTTPException
from starlette import status

from storage.film.crud import film_storage
from schemas import Films

log = logging.getLogger(__name__)


def prefetch_film(
    slug: str,
) -> Films:

    if film := film_storage.get_by_slug(slug=slug):
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug} not found.",
    )
