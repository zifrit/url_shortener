from typing import Annotated

from fastapi import APIRouter, Request, Depends

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
