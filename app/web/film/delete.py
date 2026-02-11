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

router = APIRouter(prefix="/delete")


@router.post("/{slug}", name="film:delete")
def delete_film(
    request: Request,
    film: FilmBySlug,
    storage: GetFilmStorage,
) -> RedirectResponse:
    context: dict[str, Any] = {}
    context.update(film=film)
    storage.delete(film)
    return RedirectResponse(
        request.url_for("film:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
