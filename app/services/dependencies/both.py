from typing import Mapping, Any

from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from api.jinja_temp import templates


class FormResponseHelper:
    def __init__(
        self,
        model: type[BaseModel],
        template_name: str,
    ) -> None:
        self.model = model
        self.template_name = template_name

    @classmethod
    def format_pydantic_errors(
        cls,
        error: ValidationError,
    ) -> dict[str, str]:
        return {f"{error["loc"][0]}": error["msg"] for error in error.errors()}

    def render(
        self,
        request: Request,
        *,
        form_data: type[BaseModel] | Mapping[str, Any] | None = None,
        errors: dict[str, str] | None = None,
        pydentic_error: ValidationError | None = None,
        validated: bool = False,
    ) -> HTMLResponse:
        context: dict[str, Any] = {}

        if pydentic_error:
            errors = self.format_pydantic_errors(pydentic_error)

        context.update(
            create_schema=self.model.model_json_schema(),
            error=errors,
            validated=True,
            from_data=form_data,
        )
        return templates.TemplateResponse(
            request=request,
            name=self.template_name,
            context=context,
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
                if validated and errors
                else status.HTTP_200_OK
            ),
        )
