from fastapi import APIRouter
from starlette import status

from schemas import ShortUrl, ShortUrlParticularUpdate, ShortUrlRead, ShortUrlUpdate
from services.dependencies.url_shortener import ShortUrlBySlug
from storage.short_ulr.crud import storage

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
