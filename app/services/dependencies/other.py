from typing import Annotated

from fastapi import Header, status, HTTPException, Request
from core.config import API_TOKENS
from services.dependencies.url_shortener import UNSAFE_METHODS


def api_token_validate(
    request: Request,
    token: Annotated[
        str,
        Header(alias="x-auth-token"),
    ] = "",
):

    if request.method not in UNSAFE_METHODS:
        return
    if token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
