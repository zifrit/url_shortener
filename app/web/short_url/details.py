from typing import Any

from fastapi import Request, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from api.jinja_temp import templates
from schemas.short_url import ShortUrlCreate
from services.dependencies.both import FormResponseHelper
from services.dependencies.url_shortener import GetShortUrlStorage
from storage.short_ulr.exceptions import AlreadyExistsShortUrlError

create_from_response = FormResponseHelper(
    model=ShortUrlCreate,
    template_name="short_url/create.html",
)
router = APIRouter(prefix="/create")


@router.post("/", name="short_url:create", response_model=None)
async def create_short_url(
    storage: GetShortUrlStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            data = ShortUrlCreate.model_validate(form)
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
            url=request.url_for("short_url:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except AlreadyExistsShortUrlError:
        errors = {"slug": f"Short URL with this slug={data.slug!r} already exists"}
        return create_from_response.render(
            errors=errors,
            form_data=data,
            request=request,
            validated=True,
        )


@router.get("/", name="short_url:create-view")
def get_short_url_form(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(create_schema=ShortUrlCreate.model_json_schema())
    return templates.TemplateResponse(
        request=request,
        name="short_url/create.html",
        context=context,
    )
