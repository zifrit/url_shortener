from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from api.jinja_temp import templates
from schemas.films import FilmsCreate
from services.dependencies.films import GetFilmStorage
from storage.film.exception import AlreadyExistFilmError

router = APIRouter(prefix="/create")


def create_view_validate_response(
    errors: dict[str, str],
    data: FilmsCreate | Mapping[str, Any],
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(
        create_schema=FilmsCreate.model_json_schema(),
        error=errors,
        validated=True,
        from_data=data,
    )
    return templates.TemplateResponse(
        request=request,
        name="film/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def format_pydantic_errors(error: ValidationError) -> dict[str, str]:
    return {f"{error["loc"][0]}": error["msg"] for error in error.errors()}


@router.post("/", name="film:create", response_model=None)
async def create_film(
    storage: GetFilmStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            data = FilmsCreate.model_validate(form)
        except ValidationError as error:
            errors = format_pydantic_errors(error)
            return create_view_validate_response(
                errors=errors,
                data=form,
                request=request,
            )
    try:
        storage.create_or_raise_if_exists(data)
        return RedirectResponse(
            url=request.url_for("film:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except AlreadyExistFilmError:
        errors = {"slug": f"Film with this slug={data.slug!r} already exists"}
        return create_view_validate_response(
            errors=errors,
            data=data,
            request=request,
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
