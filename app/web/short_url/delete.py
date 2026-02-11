from typing import Any, Annotated
from fastapi import APIRouter, Form, status
from starlette.requests import Request
from services.dependencies.url_shortener import ShortUrlBySlug, GetShortUrlStorage
from starlette.responses import RedirectResponse

router = APIRouter(prefix="/delete")


@router.post("/{slug}", name="short_url:delete")
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
