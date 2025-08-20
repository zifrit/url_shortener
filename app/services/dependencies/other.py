from typing import Annotated

from fastapi import Query, status, HTTPException
from core.config import API_TOKENS


def api_token_validate(
    token: Annotated[
        str,
        Query(),
    ],
):
    if token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
