from typing import Annotated
from fastapi import APIRouter, Request, status, Body, HTTPException
from api.v1.url_shortener.crud import storage
from schemas import ShortUrl, ShortUrlCreate, ShortUrlRead

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
    if not storage.get_by_slug(short_url_create.slug):
        return storage.create(short_url_create)
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Short URL with this slug={short_url_create.slug!r} already exists",
    )
