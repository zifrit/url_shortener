import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from starlette import status

from schemas import ShortUrl
from storage.short_ulr.crud import ShortUrlStorage

log = logging.getLogger(__name__)


def get_short_url_storage(request: Request) -> ShortUrlStorage:
    return request.app.state.short_url_storage  # type: ignore[no-any-return]


GetShortUrlStorage = Annotated[
    ShortUrlStorage,
    Depends(get_short_url_storage),
]


def prefetch_slug_url(
    slug: str,
    storage: GetShortUrlStorage,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'"{slug}" Not found.',
    )


ShortUrlBySlug = Annotated[
    ShortUrl,
    Depends(prefetch_slug_url),
]
