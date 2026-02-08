from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError, BaseModel

from api.jinja_temp import templates
from schemas.short_url import ShortUrlCreate, ShortUrlUpdate, ShortUrl
from services.dependencies.both import FormResponseHelper
from services.dependencies.url_shortener import GetShortUrlStorage
from storage.short_ulr.exceptions import AlreadyExistsShortUrlError

router = APIRouter(prefix="/create")

create_from_response = FormResponseHelper(
    model=ShortUrlCreate,
    template_name="short_url/create.html",
)


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


update_from_response = FormResponseHelper(
    model=ShortUrlUpdate,
    template_name="short_url/update.html",
)


@router.get("/{slug}", name="short_url:details")
def get_short_url(
    request: Request,
    slug: str,
    storage: GetShortUrlStorage,
) -> HTMLResponse:
    from_data: ShortUrl | None = storage.get_by_slug(slug=slug)
    if from_data:
        from_data: dict[str, Any] = from_data.model_dump()
    return update_from_response.render(
        form_data=from_data,
        request=request,
    )
