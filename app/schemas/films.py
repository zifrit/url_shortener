from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel


class FilmsBase(BaseModel):
    film_id: int
    name: str
    description: str
    author: str | None


class FilmsCreate(BaseModel):
    name: Annotated[
        str,
        Len(min_length=1, max_length=10),
    ]
    description: str
    author: str | None


class Films(FilmsBase):
    """
    Films model
    """
