from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from api.jinja_temp import templates
from schemas.short_url import ShortUrlCreate
from services.dependencies.url_shortener import GetShortUrlStorage

router = APIRouter(prefix="/create")


@router.post("/", name="short_url:create")
def create_short_url(
    data: Annotated[ShortUrlCreate, Form()],
    storage: GetShortUrlStorage,
    request: Request,
) -> RedirectResponse:
    storage.create_or_raise_if_exists(data)
    return RedirectResponse(
        url=request.url_for("short_url:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/", name="short_url:create-view")
def get_short_url_form(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(create_schema=ShortUrlCreate.model_json_schema())
    return templates.TemplateResponse(
        request=request,
        name="short_url/create.html",
        context=context,
    )
