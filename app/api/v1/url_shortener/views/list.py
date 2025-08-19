from typing import Annotated
from fastapi import APIRouter, Request, status, Body, BackgroundTasks
from api.v1.url_shortener.crud import storage
from schemas import ShortUrl, ShortUrlCreate, ShortUrlRead

router = APIRouter(prefix="/short-urls")


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
    background_task: BackgroundTasks,
) -> ShortUrl:
    short_url = storage.create(short_url_create)
    background_task.add_task(storage.save)
    return short_url
