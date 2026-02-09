from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, HttpUrl

from core.config import DESCRIPTION_MAX_LENGTH

DescriptionString = Annotated[str, Len(max_length=DESCRIPTION_MAX_LENGTH)]


class ShortUrlBase(BaseModel):
    target_url: HttpUrl
    description: DescriptionString = ""


class ShortUrlCreate(ShortUrlBase):
    """
    ShortUrl create schema
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class ShortUrlUpdate(ShortUrlBase):
    """
    ShortUrlUpdate model for update short url
    """

    description: DescriptionString = ""


class ShortUrlParticularUpdate(BaseModel):
    """
    ShortUrlParticularUpdate model for particular update short url
    """

    target_url: HttpUrl | None = None
    description: DescriptionString | None = None


class ShortUrlRead(ShortUrlBase):
    """
    ShortUrlRead model
    """

    slug: str


class ShortUrl(ShortUrlBase):
    """
    ShortUrl model
    """

    slug: str
