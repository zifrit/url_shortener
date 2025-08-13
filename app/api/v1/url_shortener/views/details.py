from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.v1.url_shortener.crud import storage
from schemas import ShortUrl
from services.dependencies.url_shortener import prefetch_slug_url

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
    response_model=ShortUrl,
)
def info_short_urls(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
) -> ShortUrl:
    return url


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
) -> None:
    storage.delete(url)
