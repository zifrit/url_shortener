from fastapi import HTTPException
from starlette import status

from api.v1.films.crud import fim_storage
from schemas import Films


def prefetch_film(
    slug: str,
) -> Films:

    if film := fim_storage.get_by_slug(slug=slug):
        return film
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug} not found.",
    )
