from fastapi import HTTPException, BackgroundTasks
from starlette import status

from api.v1.url_shortener.crud import storage
from schemas import ShortUrl


def prefetch_slug_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'"{slug}" Not found.',
    )


def save_short_url_state(
    background_task: BackgroundTasks,
):
    yield
    background_task.add_task(storage.save)
