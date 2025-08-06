from pydantic import BaseModel


class FilmsBase(BaseModel):
    film_id: int
    name: str
    description: str
    author: str | None


class Films(FilmsBase):
    """
    Films model
    """
