from typing import Annotated, Any

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from api.jinja_temp import templates
from schemas.short_url import ShortUrlCreate
from services.dependencies.url_shortener import GetShortUrlStorage
from storage.short_ulr.exceptions import AlreadyExistsShortUrlError

router = APIRouter(prefix="/create")


@router.post("/", name="short_url:create", response_model=None)
def create_short_url(
    data: Annotated[ShortUrlCreate, Form()],
    storage: GetShortUrlStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    try:
        storage.create_or_raise_if_exists(data)
        return RedirectResponse(
            url=request.url_for("short_url:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except AlreadyExistsShortUrlError:
        error = {"slug": f"Short URL with this slug={data.slug!r} already exists"}
        context: dict[str, Any] = {}
        context.update(
            create_schema=ShortUrlCreate.model_json_schema(),
            error=error,
            validated=True,
            from_data=data,
        )
        return templates.TemplateResponse(
            request=request,
            name="short_url/create.html",
            context=context,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
