import logging
from typing import Annotated

from fastapi import Depends, status, HTTPException, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)
from core.config import API_TOKENS, USERS, REDIS_TOKENS_SET_NAME
from services.dependencies.url_shortener import UNSAFE_METHODS
from services.frameworks.cache import cache_token_storage

log = logging.getLogger(__name__)

security = HTTPBearer(
    scheme_name="Static API Token",
    description="Your static API token from the developer portal",
    auto_error=False,
)

base_security = HTTPBasic(
    scheme_name="Base auth",
    description="Your Base auth from the developer portal",
    auto_error=False,
)


def api_token_validate(token: HTTPAuthorizationCredentials):

    log.info("API token %s", token)
    if not cache_token_storage.token_exists(
        token.credentials,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def api_token_auth(
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
    api_token_validate(token)


def username_password_validate(cred: HTTPBasicCredentials | None):

    log.info("Credentials %s", cred)
    if cred and cred.username in USERS and USERS[cred.username] == cred.password:
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username and password are required",
        headers={"WWW-Authenticate": "Basic"},
    )


def username_password_auth(
    request: Request,
    cred: Annotated[
        HTTPBasicCredentials | None,
        Depends(base_security),
    ] = None,
):

    if request.method not in UNSAFE_METHODS:
        return

    username_password_validate(cred)


def combine_auth(
    request: Request,
    token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security),
    ] = None,
    cred: Annotated[
        HTTPBasicCredentials | None,
        Depends(base_security),
    ] = None,
):

    if request.method not in UNSAFE_METHODS:
        return

    if token:
        return api_token_validate(token)
    if cred:
        return username_password_validate(cred)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Api token or base auth are required",
    )
