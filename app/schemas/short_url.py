from pydantic import BaseModel, HttpUrl


class ShortUrlBase(BaseModel):
    taget_url: HttpUrl
    slug: str


class ShortUrl(ShortUrlBase):
    """
    ShortUrl model
    """
