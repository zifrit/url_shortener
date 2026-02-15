from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from services.dependencies.films import FilmBySlug, GetFilmStorage

router = APIRouter(prefix="/delete/{slug}")


@router.post("/", name="film:delete")
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
