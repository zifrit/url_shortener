from unittest import TestCase

from pydantic import ValidationError

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
            target_url="https://example.com",
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
            short_url_in.target_url,
            short_url.target_url,
        )

    def test_short_url_can_be_updated_from_update_schemas(self) -> None:
        short_url = ShortUrl(
            slug="some-slug",
            description="some-description",
            target_url="https://example.com",
        )
        updated_short_url = ShortUrlUpdate(
            target_url="https://example.com",
            description="some-new-description",
        )

        for key, value in updated_short_url:
            setattr(short_url, key, value)

        self.assertEqual(
            updated_short_url.description,
            short_url.description,
        )
        self.assertEqual(
            updated_short_url.target_url,
            short_url.target_url,
        )

    def test_short_url_can_be_particular_update_from_update_schemas(self) -> None:
        short_url = ShortUrl(
            slug="some-slug",
            description="some-description",
            target_url="https://example.com",
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

        self.assertEqual(
            "https://example.com/",
            short_url.target_url.__str__(),
        )

        short_url = ShortUrl(
            slug="some-slug",
            description="some-description",
            target_url="https://example.com",
        )

        updated_short_url = ShortUrlParticularUpdate()

        for key, value in updated_short_url.model_dump(exclude_unset=True).items():
            setattr(short_url, key, value)

        self.assertEqual(
            "https://example.com/",
            short_url.target_url.__str__(),
        )

        self.assertEqual(
            "some-description",
            short_url.description,
        )

    def test_short_url_create_accepts_different_urls(self) -> None:
        urls = [
            "http://example.com",
            "https://example",
            "https://goggle",
            # "rtmp://video.example.com",
            # "rtmps://video.example.com",
            "http://abc.example.com",
            "https://www.example.com/some-test/",
        ]

        for url in urls:
            with self.subTest(msg=f"test-url-{url}"):
                short_url_create = ShortUrlCreate(
                    slug="some-slug",
                    description="some-description",
                    target_url=url,
                )
                self.assertEqual(
                    url.rstrip("/"),
                    short_url_create.model_dump(mode="json")["target_url"].rstrip("/"),
                )

    def test_short_url_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            ShortUrlCreate(
                slug="s",
                description="some-description",
                target_url="https://example.com",
            )
        error_details = exc_info.exception.errors()[0]
        expect_type = "string_too_short"
        self.assertEqual(
            expect_type,
            error_details["type"],
        )

    def test_short_url_slug_too_shore_regx(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            "String should have at least 3 characters",
        ):
            ShortUrlCreate(
                slug="s",
                description="some-description",
                target_url="https://example.com",
            )
