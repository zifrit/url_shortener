from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.jinja_temp import templates
from services.dependencies.films import GetFilmStorage

router = APIRouter()


@router.get("/list", name="film:list")
def list_film(
    request: Request,
    storage: GetFilmStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(list_of_films=storage.get())
    return templates.TemplateResponse(
        request=request,
        name="film/list.html",
        context=context,
    )
