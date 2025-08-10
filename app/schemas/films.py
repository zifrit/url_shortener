from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel


class FilmsBase(BaseModel):
    slug: str
    name: str
    description: str
    author: str | None


class FilmsCreate(FilmsBase):
    """
    create films model
    """

    name: Annotated[
        str,
        Len(min_length=1, max_length=10),
    ]


class Films(FilmsBase):
    """
    Films model
    """
