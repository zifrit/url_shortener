from typing import Annotated

from fastapi import Depends, status, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.config import API_TOKENS
from services.dependencies.url_shortener import UNSAFE_METHODS


security = HTTPBearer(
    scheme_name="Static API Token",
    description="Your static API token from the developer portal",
    auto_error=False,
)


def api_token_validate(
    request: Request,
    token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security),
    ] = None,
):

    if request.method not in UNSAFE_METHODS:
        return
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )
    if token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
