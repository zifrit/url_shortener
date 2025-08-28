from unittest import TestCase

from schemas.short_url import ShortUrl, ShortUrlCreate


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
