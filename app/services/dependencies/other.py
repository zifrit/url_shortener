import logging
from typing import Annotated

from fastapi import Depends, status, HTTPException, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)
from services.dependencies.url_shortener import UNSAFE_METHODS
from api.v1.auth.services.by_token import cache_token_storage
from api.v1.auth.services.by_username_and_password import cache_user_storage

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
    if cred and cache_user_storage.validate_user_password(cred.username, cred.password):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        # headers={"WWW-Authenticate": "Basic"},
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
