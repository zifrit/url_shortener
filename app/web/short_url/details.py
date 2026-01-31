from typing import Annotated, Any

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from api.jinja_temp import templates
from schemas.short_url import ShortUrlCreate

router = APIRouter(prefix="/create")


@router.post("/", name="short_url:create")
def create_short_url(data: Annotated[ShortUrlCreate, Form()]):
    return data.model_dump(mode="json")


@router.get("/", name="short_url:create-view")
def get_short_url_form(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(create_schema=ShortUrlCreate.model_json_schema())
    return templates.TemplateResponse(
        request=request,
        name="short_url/create.html",
        context=context,
    )
