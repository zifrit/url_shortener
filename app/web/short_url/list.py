from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.jinja_temp import templates

router = APIRouter()


@router.get("/list", name="short_url:list")
def list_short_urls(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="short_url/list.html",
        context={},
    )
