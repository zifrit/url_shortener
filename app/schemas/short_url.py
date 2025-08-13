from typing import Annotated
from annotated_types import Len
from pydantic import BaseModel, HttpUrl


class ShortUrlBase(BaseModel):
    taget_url: HttpUrl
    description: Annotated[
        str,
        Len(max_length=200),
    ] = ""


class ShortUrlCreate(ShortUrlBase):
    """
    ShortUrl create schema
    """

    slug: Annotated[
        str,
        Len(min_length=1, max_length=10),
    ]


class ShortUrlUpdate(ShortUrlBase):
    """
    ShortUrlUpdate model for update short url
    """

    description: Annotated[
        str,
        Len(max_length=200),
    ]


class ShortUrl(ShortUrlBase):
    """
    ShortUrl model
    """

    slug: str
