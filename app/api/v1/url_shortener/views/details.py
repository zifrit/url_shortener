from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status

from app.api.v1.url_shortener.crud import storage
from app.schemas import ShortUrl, ShortUrlUpdate, ShortUrlParticularUpdate, ShortUrlRead
from app.services.dependencies.url_shortener import prefetch_slug_url

router = APIRouter(
    prefix="/{slug}",
    responses={
        # status.HTTP_204_NO_CONTENT: None,
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    },
                },
            },
        },
    },
)

ShortUrlBySlug = Annotated[
    ShortUrl,
    Depends(prefetch_slug_url),
]


@router.get(
    "/",
    response_model=ShortUrlRead,
)
def info_short_urls(
    url: ShortUrlBySlug,
) -> ShortUrl:
    return url


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: ShortUrlBySlug,
) -> None:
    storage.delete(url)


@router.put("/", status_code=status.HTTP_200_OK, response_model=ShortUrlRead)
def update_short_url_details(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlUpdate,
) -> ShortUrl:
    return storage.update(short_url=url, short_url_in=short_url_in)


@router.patch("/", status_code=status.HTTP_200_OK, response_model=ShortUrlRead)
def particular_update_short_url_details(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlParticularUpdate,
) -> ShortUrl:
    return storage.particular_update(short_url=url, short_url_in=short_url_in)
