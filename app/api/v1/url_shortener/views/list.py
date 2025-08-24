from typing import Annotated
from fastapi import APIRouter, Request, status, Body, HTTPException
from api.v1.url_shortener.crud import storage, AlreadyExistsShortUrlError
from schemas import ShortUrl, ShortUrlCreate, ShortUrlRead
from typing import cast

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
