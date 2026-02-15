from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from schemas.films import FilmsUpdate
from services.dependencies.both import FormResponseHelper
from services.dependencies.films import FilmBySlug, GetFilmStorage

router = APIRouter(prefix="/update/{slug}")


update_from_response = FormResponseHelper(
    model=FilmsUpdate,
    template_name="film/update.html",
)


@router.get("/", name="film:details")
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


@router.post("/", name="film:update", response_model=None)
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
