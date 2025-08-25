from typing import Annotated, cast

from app.api.v1.url_shortener.crud import AlreadyExistsShortUrlError, storage
from app.schemas import ShortUrl, ShortUrlCreate, ShortUrlRead
from fastapi import APIRouter, Body, HTTPException, Request, status

router = APIRouter(
    prefix="/short-urls",
)


@router.get("/", response_model=list[ShortUrlRead])
def read_short_url_list(request: Request) -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Invalid request",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short URL with slug='foobar' already exists."
                    },
                },
            },
        },
    },
)
def create_short_url(
    short_url_create: Annotated[ShortUrlCreate, Body()],
) -> ShortUrl:
    try:
        return cast(
            ShortUrl, storage.create_or_raise_if_exists(short_url=short_url_create)
        )
    except AlreadyExistsShortUrlError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with this slug={short_url_create.slug!r} already exists",
        )
