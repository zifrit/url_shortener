from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.jinja_temp import templates
from services.dependencies.url_shortener import GetShortUrlStorage

router = APIRouter()


@router.get("/list", name="short_url:list")
def list_short_urls(
    request: Request,
    storage: GetShortUrlStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(list_of_short_urls=storage.get())
    return templates.TemplateResponse(
        request=request,
        name="short_url/list.html",
        context=context,
    )
