import logging

from fastapi import HTTPException, BackgroundTasks, Request
from starlette import status

from api.v1.url_shortener.crud import storage
from schemas import ShortUrl

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)

log = logging.getLogger(__name__)


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
    request: Request,
    background_task: BackgroundTasks,
):
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage")
        background_task.add_task(storage.save)
