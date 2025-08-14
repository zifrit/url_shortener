from typing import Annotated
from annotated_types import Len
from pydantic import BaseModel, HttpUrl


DescriptionString = Annotated[str, Len(max_length=200)]


class ShortUrlBase(BaseModel):
    taget_url: HttpUrl
    description: DescriptionString = ""


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

    description: DescriptionString


class ShortUrlParticularUpdate(ShortUrlBase):
    """
    ShortUrlParticularUpdate model for particular update short url
    """

    taget_url: HttpUrl | None = None
    description: DescriptionString | None = None


class ShortUrl(ShortUrlBase):
    """
    ShortUrl model
    """

    slug: str
