from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status

from api.v1.url_shortener.crud import storage
from schemas import ShortUrl, ShortUrlUpdate, ShortUrlParticularUpdate, ShortUrlRead
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
    background_task: BackgroundTasks,
) -> None:
    background_task.add_task(storage.save)
    storage.delete(url)


@router.put("/", status_code=status.HTTP_200_OK, response_model=ShortUrlRead)
def update_short_url_details(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlUpdate,
    background_task: BackgroundTasks,
) -> ShortUrl:
    short_url = storage.update(short_url=url, short_url_in=short_url_in)
    background_task.add_task(storage.save)
    return short_url


@router.patch("/", status_code=status.HTTP_200_OK, response_model=ShortUrlRead)
def particular_update_short_url_details(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlParticularUpdate,
    background_task: BackgroundTasks,
) -> ShortUrl:
    background_task.add_task(storage.save)
    short_url = storage.particular_update(short_url=url, short_url_in=short_url_in)
    background_task.add_task(storage.save)
    return short_url
