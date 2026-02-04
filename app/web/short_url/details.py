from typing import Annotated, Any, Mapping

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from api.jinja_temp import templates
from schemas.short_url import ShortUrlCreate
from services.dependencies.url_shortener import GetShortUrlStorage
from storage.short_ulr.exceptions import AlreadyExistsShortUrlError

router = APIRouter(prefix="/create")


def create_view_validate_response(
    errors: dict[str, str],
    data: ShortUrlCreate | Mapping[str, Any],
    request: Request,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    context.update(
        create_schema=ShortUrlCreate.model_json_schema(),
        error=errors,
        validated=True,
        from_data=data,
    )
    return templates.TemplateResponse(
        request=request,
        name="short_url/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def format_pydantic_errors(errors: list[dict[str, Any]]) -> dict[str, str]:
    return {error["loc"][0]: error["msg"] for error in errors}


@router.post("/", name="short_url:create", response_model=None)
async def create_short_url(
    storage: GetShortUrlStorage,
    request: Request,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            data = ShortUrlCreate.model_validate(form)
        except ValidationError as error:
            errors = format_pydantic_errors(error.errors())
            return create_view_validate_response(
                errors=errors,
                data=form,
                request=request,
            )
    try:
        storage.create_or_raise_if_exists(data)
        return RedirectResponse(
            url=request.url_for("short_url:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except AlreadyExistsShortUrlError:
        errors = {"slug": f"Short URL with this slug={data.slug!r} already exists"}
        return create_view_validate_response(
            errors=errors,
            data=data,
            request=request,
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
