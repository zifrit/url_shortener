from typing import Annotated
from annotated_types import Len
from fastapi import APIRouter, Request, Depends, status, Form
from pydantic import HttpUrl
from api.v1.url_shortener.crud import SHORT_URL
from schemas import ShortUrl
from services.dependencies.url_shortener import prefetch_slug_url

router = APIRouter(prefix="/short-urls")


@router.get("/", response_model=list[ShortUrl])
def read_short_url_list(request: Request) -> list[ShortUrl]:
    return SHORT_URL


@router.get(
    "/{slug}/",
    response_model=ShortUrl,
)
def info_short_urls(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_slug_url),
    ],
):
    return url


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    taget_url: Annotated[HttpUrl, Form()],
    slug: Annotated[
        str,
        Len(max_length=10, min_length=2),
        Form(),
    ],
) -> ShortUrl:
    return ShortUrl(
        taget_url=taget_url,
        slug=slug,
    )
