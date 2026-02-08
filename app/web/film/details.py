from collections.abc import Mapping
from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from api.jinja_temp import templates
from schemas.films import FilmsCreate, FilmsUpdate, Films
from services.dependencies.both import FormResponseHelper
from services.dependencies.films import GetFilmStorage
from storage.film.exception import AlreadyExistFilmError

router = APIRouter(prefix="/create")


create_from_response = FormResponseHelper(
    model=FilmsCreate,
    template_name="film/create.html",
)


@router.post("/", name="film:create", response_model=None)
async def create_film(
    storage: GetFilmStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            data = FilmsCreate.model_validate(form)
        except ValidationError as error:
            return create_from_response.render(
                request=request,
                pydentic_error=error,
                form_data=form,
                validated=True,
            )
    try:
        storage.create_or_raise_if_exists(data)
        return RedirectResponse(
            url=request.url_for("film:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except AlreadyExistFilmError:
        errors = {"slug": f"Film with this slug={data.slug!r} already exists"}
        return create_from_response.render(
            errors=errors,
            form_data=data,
            request=request,
            validated=True,
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


update_from_response = FormResponseHelper(
    model=FilmsUpdate,
    template_name="film/update.html",
)


@router.get("/{slug}", name="film:details")
def get_film(
    request: Request,
    slug: str,
    storage: GetFilmStorage,
) -> HTMLResponse:
    from_data: Films | None = storage.get_by_slug(slug=slug)
    if from_data:
        from_data: dict[str, Any] = from_data.model_dump()
    return update_from_response.render(
        form_data=from_data,
        request=request,
    )
