import logging

from fastapi import HTTPException, BackgroundTasks, Request
from starlette import status

from api.v1.films.crud import film_storage
from schemas import Films
from .url_shortener import UNSAFE_METHODS

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
