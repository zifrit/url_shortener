from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.jinja_temp import templates

router = APIRouter(
    include_in_schema=False,
)


@router.get(
    "/",
    name="home",
    response_class=HTMLResponse,
)
def read_root(
    request: Request,
) -> HTMLResponse:
    context: dict[str, list[str]] = {
        "features": [
            "User Authentication with OTP",
            "Dynamic Content Rendering",
            "Responsive Design",
            "Easy Navigation",
            "Secure Data Handling",
        ],
    }
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )


@router.get(
    "/about",
    name="about",
    response_class=HTMLResponse,
)
def read_about(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={},
    )
