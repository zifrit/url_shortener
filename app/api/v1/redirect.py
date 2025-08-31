from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from schemas import ShortUrl

SHORT_URL = [
    ShortUrl(
        target_url=HttpUrl("https://www.google.com"),
        slug="google",
    ),
    ShortUrl(
        target_url=HttpUrl("https://www.example.com"),
        slug="search",
    ),
]

router = APIRouter(prefix="/r")


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


@router.get("/{slug}/")
def redirect_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
) -> RedirectResponse:
    return RedirectResponse(url=str(url.target_url))
