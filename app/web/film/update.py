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


@router.post("/{slug}", name="film:update")
def update_film(
    request: Request,
    film_in: Annotated[FilmsUpdate, Form()],
    film: FilmBySlug,
    storage: GetFilmStorage,
) -> RedirectResponse:
    storage.update(
        film=film,
        film_in=film_in,
    )
    return RedirectResponse(
        url=request.url_for("film:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
