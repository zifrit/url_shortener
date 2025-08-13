from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel


class FilmsBase(BaseModel):
    name: str
    description: Annotated[
        str,
        Len(max_length=200),
    ] = ""
    author: str | None


class FilmsCreate(FilmsBase):
    """
    create films model
    """

    slug: str
    name: Annotated[
        str,
        Len(min_length=1, max_length=10),
    ]


class FilmsUpdate(FilmsBase):
    """
    FilmsUpdate model for update film
    """

    description: Annotated[
        str,
        Len(max_length=200),
    ]


class Films(FilmsBase):
    """
    Films model
    """

    slug: str
