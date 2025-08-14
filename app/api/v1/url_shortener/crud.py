from pydantic import BaseModel, HttpUrl
from schemas import ShortUrl, ShortUrlCreate, ShortUrlUpdate, ShortUrlParticularUpdate


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

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)

    def delete(self, short_url: ShortUrl) -> None:
        self.slug_to_short_url.pop(short_url.slug, None)

    def update(self, short_url: ShortUrl, short_url_in: ShortUrlUpdate) -> ShortUrl:
        for key, value in short_url_in:
            setattr(short_url, key, value)
        return short_url

    def particular_update(
        self, short_url: ShortUrl, short_url_in: ShortUrlParticularUpdate
    ) -> ShortUrl:
        for key, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, key, value)
        return short_url


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
