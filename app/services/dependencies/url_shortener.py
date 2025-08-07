from fastapi import HTTPException
from starlette import status

from api.v1.url_shortener.crud import SHORT_URL
from schemas import ShortUrl


def prefetch_slug_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = next(
        (url for url in SHORT_URL if url.slug == slug),
        None,
    )
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'"{slug}" Not found.',
    )
