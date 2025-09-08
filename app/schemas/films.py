from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel

DescriptionString = Annotated[str, Len(max_length=200)]


class FilmsBase(BaseModel):
    name: str
    description: DescriptionString = ""
    author: str | None


class FilmsCreate(FilmsBase):
    """
    create films model
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]
    name: Annotated[
        str,
        Len(min_length=1, max_length=10),
    ]


class FilmsUpdate(FilmsBase):
    """
    FilmsUpdate model for update film
    """

    description: DescriptionString


class FilmsParticularUpdate(BaseModel):
    """
    FilmsParticularUpdate model for particular update film
    """

    name: str | None = None
    author: str | None = None
    description: DescriptionString | None = None


class FilmsRead(FilmsBase):
    """
    FilmsRead model
    """

    slug: str


class Films(FilmsBase):
    """
    Films model
    """

    slug: str
