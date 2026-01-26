from datetime import UTC, datetime

from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR


def inject_current_date_and_time(
    request: Request,  # noqa: ARG001
) -> dict[str, datetime]:
    return {
        "today": datetime.now(tz=UTC),
    }


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates"),
    context_processors=[inject_current_date_and_time],
)
