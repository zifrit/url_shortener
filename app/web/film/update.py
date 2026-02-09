from collections.abc import Mapping
from typing import Any, Annotated

from fastapi import APIRouter, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from api.jinja_temp import templates
from schemas.films import FilmsCreate, FilmsUpdate, Films
from services.dependencies.both import FormResponseHelper
from services.dependencies.films import GetFilmStorage, FilmBySlug
from storage.film.exception import AlreadyExistFilmError

router = APIRouter(prefix="/update")


update_from_response = FormResponseHelper(
    model=FilmsUpdate,
    template_name="film/update.html",
)


@router.get("/{slug}", name="film:details")
def get_film(
    request: Request,
    film: FilmBySlug,
) -> HTMLResponse:
    from_data: dict[str, Any] = FilmsUpdate(**film.model_dump()).model_dump()
    return update_from_response.render(
        form_data=from_data,
        request=request,
        film=film,
    )


@router.post("/{slug}", name="film:update", response_model=None)
async def update_film(
    request: Request,
    film: FilmBySlug,
    storage: GetFilmStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            film_in = FilmsUpdate.model_validate(form)
        except ValidationError as error:
            return update_from_response.render(
                request=request,
                pydentic_error=error,
                form_data=form,
                validated=True,
                film=film,
            )
    storage.update(
        film=film,
        film_in=film_in,
    )
    return RedirectResponse(
        url=request.url_for("film:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
