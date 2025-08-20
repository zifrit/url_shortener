import logging
from typing import Annotated

from fastapi import Depends, status, HTTPException, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)
from core.config import API_TOKENS, USERS
from services.dependencies.url_shortener import UNSAFE_METHODS

log = logging.getLogger(__name__)

security = HTTPBearer(
    scheme_name="Static API Token",
    description="Your static API token from the developer portal",
    auto_error=False,
)

base_security = HTTPBasic(
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
    log.info("API token %s", token)
    if token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def username_password_validate(
    request: Request,
    cred: Annotated[
        HTTPBasicCredentials | None,
        Depends(base_security),
    ] = None,
):

    if request.method not in UNSAFE_METHODS:
        return
    log.info("Credentials %s", cred)
    if cred and cred.username in USERS and USERS[cred.username] == cred.password:
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username and password are required",
        headers={"WWW-Authenticate": "Basic"},
    )
