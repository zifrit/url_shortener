from pydantic import BaseModel, HttpUrl
from schemas import ShortUrl, ShortUrlCreate


class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, data: ShortUrlCreate) -> ShortUrl:
        new_short_url = ShortUrl(**data.model_dump())
        self.slug_to_short_url[new_short_url.slug] = new_short_url
        return new_short_url


storage = ShortUrlStorage()

storage.create(
    ShortUrlCreate(
        taget_url=HttpUrl("https://www.google.com"),
        slug="google",
    ),
)
storage.create(
    ShortUrlCreate(
        taget_url=HttpUrl("https://www.example.com"),
        slug="search",
    ),
)
