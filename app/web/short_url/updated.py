from typing import Any, Annotated

from fastapi import APIRouter, Form, status
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from schemas import ShortUrlUpdate
from services.dependencies.both import FormResponseHelper
from services.dependencies.url_shortener import ShortUrlBySlug, GetShortUrlStorage

router = APIRouter(prefix="/update")

update_from_response = FormResponseHelper(
    model=ShortUrlUpdate,
    template_name="short_url/update.html",
)


@router.get("/{slug}", name="short_url:details")
def get_short_url(
    request: Request,
    short_url: ShortUrlBySlug,
) -> HTMLResponse:
    from_data: dict[str, Any] = ShortUrlUpdate(**short_url.model_dump()).model_dump()
    return update_from_response.render(
        form_data=from_data,
        request=request,
        short_url=short_url,
    )


@router.post("/{slug}", name="short_url:update", response_model=None)
async def update_short_url(
    request: Request,
    short_url: ShortUrlBySlug,
    storage: GetShortUrlStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            short_url_in = ShortUrlUpdate.model_validate(form)
        except ValidationError as error:
            return update_from_response.render(
                request=request,
                pydentic_error=error,
                form_data=form,
                validated=True,
                short_url=short_url,
            )
    storage.update(
        short_url=short_url,
        short_url_in=short_url_in,
    )
    return RedirectResponse(
        url=request.url_for("short_url:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
