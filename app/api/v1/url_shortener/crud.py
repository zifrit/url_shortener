from pydantic import BaseModel, ValidationError, HttpUrl

from core import SHORT_URL_DIR
from schemas import ShortUrl, ShortUrlCreate, ShortUrlUpdate, ShortUrlParticularUpdate


class ShortUrlStorage(BaseModel):
    slug_to_item: dict[str, ShortUrl] = {}

    def save(self) -> None:
        SHORT_URL_DIR.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls) -> "ShortUrlStorage":
        if not SHORT_URL_DIR.exists():
            return ShortUrlStorage()
        return cls.model_validate_json(SHORT_URL_DIR.read_text())

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_item.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_item.get(slug)

    def create(self, data: ShortUrlCreate) -> ShortUrl:
        new_short_url = ShortUrl(**data.model_dump())
        self.slug_to_item[new_short_url.slug] = new_short_url
        self.save()
        return new_short_url

    def delete_by_slug(self, slug: str) -> None:
        self.save()
        self.slug_to_item.pop(slug, None)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(short_url.slug)

    def update(self, short_url: ShortUrl, short_url_in: ShortUrlUpdate) -> ShortUrl:
        for key, value in short_url_in:
            setattr(short_url, key, value)
        self.save()
        return short_url

    def particular_update(
        self, short_url: ShortUrl, short_url_in: ShortUrlParticularUpdate
    ) -> ShortUrl:
        for key, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, key, value)
        self.save()
        return short_url


try:
    storage = ShortUrlStorage.load()
except ValidationError:
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
