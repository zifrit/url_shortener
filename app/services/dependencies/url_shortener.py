import logging

from app.api.v1.url_shortener.crud import storage
from app.schemas import ShortUrl
from fastapi import HTTPException
from starlette import status

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)

log = logging.getLogger(__name__)


def prefetch_slug_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'"{slug}" Not found.',
    )
