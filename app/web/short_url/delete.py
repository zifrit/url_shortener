from typing import Any

from fastapi import APIRouter, status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from services.dependencies.url_shortener import GetShortUrlStorage, ShortUrlBySlug

router = APIRouter(prefix="/delete/{slug}")


@router.post("/", name="short_url:delete")
def delete_short_url(
    request: Request,
    short_url: ShortUrlBySlug,
    storage: GetShortUrlStorage,
) -> RedirectResponse:
    context: dict[str, Any] = {}
    context.update(short_url=short_url)
    storage.delete(short_url)
    return RedirectResponse(
        request.url_for("short_url:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
