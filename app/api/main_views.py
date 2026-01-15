from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from api.jinja_temp import templates

router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def read_root(
    request: Request,
) -> HTMLResponse:
    context = {
        "today": datetime.now(tz="UTC"),
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
