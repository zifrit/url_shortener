from typing import Annotated
from fastapi import APIRouter, Request, Depends, status, Body
from api.v1.url_shortener.crud import storage
from schemas import ShortUrl, ShortUrlCreate
from services.dependencies.url_shortener import prefetch_slug_url

router = APIRouter(prefix="/short-urls")


@router.get("/", response_model=list[ShortUrl])
def read_short_url_list(request: Request) -> list[ShortUrl]:
    return storage.get()


@router.get(
    "/{slug}/",
    response_model=ShortUrl,
)
def info_short_urls(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
) -> ShortUrl:
    return url


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: Annotated[ShortUrlCreate, Body()],
) -> ShortUrl:
    return storage.create(short_url_create)


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
) -> None:
    storage.delete(url)
