from unittest import TestCase

from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlParticularUpdate,
    ShortUrlUpdate,
)


class ShortUrlTestCase(TestCase):
    def test_short_url_can_be_created_from_create_schemas(self) -> None:
        short_url_in = ShortUrlCreate(
            slug="some-slug",
            description="some-description",
            taget_url="https://example.com",
        )
        short_url = ShortUrl(**short_url_in.model_dump())
        self.assertEqual(
            short_url_in.slug,
            short_url.slug,
        )
        self.assertEqual(
            short_url_in.description,
            short_url.description,
        )
        self.assertEqual(
            short_url_in.taget_url,
            short_url.taget_url,
        )

    def test_short_url_can_be_updated_from_update_schemas(self) -> None:
        short_url = ShortUrl(
            slug="some-slug",
            description="some-description",
            taget_url="https://example.com",
        )
        updated_short_url = ShortUrlUpdate(
            taget_url="https://example.com",
            description="some-new-description",
        )

        for key, value in updated_short_url:
            setattr(short_url, key, value)

        self.assertEqual(
            updated_short_url.description,
            short_url.description,
        )
        self.assertEqual(
            updated_short_url.taget_url,
            short_url.taget_url,
        )

    def test_short_url_can_be_particular_update_from_update_schemas(self) -> None:
        short_url = ShortUrl(
            slug="some-slug",
            description="some-description",
            taget_url="https://example.com",
        )
        updated_short_url = ShortUrlParticularUpdate(
            description="some-new-description",
        )

        for key, value in updated_short_url.model_dump(exclude_unset=True).items():
            setattr(short_url, key, value)

        self.assertEqual(
            updated_short_url.description,
            short_url.description,
        )
