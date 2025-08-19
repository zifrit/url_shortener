from typing import Annotated
from fastapi import APIRouter, Request, status, Body, BackgroundTasks, Depends
from api.v1.url_shortener.crud import storage
from schemas import ShortUrl, ShortUrlCreate, ShortUrlRead
from services.dependencies.url_shortener import save_short_url_state

router = APIRouter(
    prefix="/short-urls",
    dependencies=[Depends(save_short_url_state)],
)


@router.get("/", response_model=list[ShortUrlRead])
def read_short_url_list(request: Request) -> list[ShortUrl]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: Annotated[ShortUrlCreate, Body()],
) -> ShortUrl:
    return storage.create(short_url_create)
