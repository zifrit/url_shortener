from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.jinja_temp import templates

router = APIRouter()


@router.get("/list", name="film:list")
def list_film(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="film/list.html",
        context={},
    )
