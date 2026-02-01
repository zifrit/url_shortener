from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from api.jinja_temp import templates
from schemas.films import FilmsCreate
from services.dependencies.films import GetFilmStorage

router = APIRouter(prefix="/create")


@router.post("/", name="film:create")
def create_film(
    data: Annotated[FilmsCreate, Form()],
    storage: GetFilmStorage,
    request: Request,
) -> RedirectResponse:
    storage.create_or_raise_if_exists(data)
    return RedirectResponse(
        url=request.url_for("film:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/", name="film:create-view")
def get_film_form(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(create_schema=FilmsCreate.model_json_schema())
    return templates.TemplateResponse(
        request=request,
        name="film/create.html",
        context=context,
    )
