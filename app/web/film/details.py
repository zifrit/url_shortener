from typing import Annotated, Any

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from api.jinja_temp import templates
from schemas.films import FilmsCreate

router = APIRouter(prefix="/create")


@router.post("/", name="film:create")
def create_film(data: Annotated[FilmsCreate, Form()]):
    return data.model_dump(mode="json")


@router.get("/", name="film:create-view")
def get_film_form(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(create_schema=FilmsCreate.model_json_schema())
    return templates.TemplateResponse(
        request=request,
        name="film/create.html",
        context=context,
    )
