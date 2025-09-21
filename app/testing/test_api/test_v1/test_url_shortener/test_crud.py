import random
import string
from typing import ClassVar
from unittest import TestCase

import pytest
from pydantic import HttpUrl

from api.v1.url_shortener.crud import AlreadyExistsShortUrlError, storage
from schemas import ShortUrl, ShortUrlCreate, ShortUrlParticularUpdate, ShortUrlUpdate


def create_short_ulr() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),
        description="some-description",
        target_url="https://example.com",
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> ShortUrl:
    return create_short_ulr()


class ShortUrlStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.short_url = create_short_ulr()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def test_update(self) -> None:
        short_url_update = ShortUrlUpdate(
            **self.short_url.model_dump(),
        )
        source_description = self.short_url.description
        source_target_url = self.short_url.target_url

        short_url_update.description = self.short_url.description * 2
        short_url_update.target_url = HttpUrl("https://new-example.com")
        updated_short_url = storage.update(
            short_url=self.short_url,
            short_url_in=short_url_update,
        )
        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )
        self.assertNotEqual(
            source_target_url,
            updated_short_url.target_url,
        )
        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(**short_url_update.model_dump()),
        )

    def test_particular_update(self) -> None:
        short_url_particular_update = ShortUrlParticularUpdate(
            description=self.short_url.description * 2,
        )

        source_description = self.short_url.description
        updated_short_url = storage.particular_update(
            short_url=self.short_url,
            short_url_in=short_url_particular_update,
        )

        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_particular_update.description,
            updated_short_url.description,
        )


class ShortUrlStorageGetTestCase(TestCase):
    SHORT_URLS_COUNT = 3
    short_urls: ClassVar[list[ShortUrl]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.short_urls = [create_short_ulr() for _ in range(cls.SHORT_URLS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for short_url in cls.short_urls:
            storage.delete(short_url)

    def test_get_list(self) -> None:
        short_urls = storage.get()
        slugs = {su.slug for su in short_urls}
        expected_slugs = {su.slug for su in self.short_urls}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for short_url in self.short_urls:
            with self.subTest(
                slug=short_url.slug,
                msg=f"Validate can get slug {short_url.slug}",
            ):
                db_short_url = storage.get_by_slug(short_url.slug)
                self.assertEqual(
                    short_url,
                    db_short_url,
                )


def test_create_or_raise_if_exists(short_url: ShortUrl) -> None:
    short_url_create = ShortUrlCreate(**short_url.model_dump())
    with pytest.raises(
        AlreadyExistsShortUrlError,
        match=short_url_create.slug,
    ) as exc_ingo:
        storage.create_or_raise_if_exists(short_url_create)

    assert exc_ingo.value.args[0] == short_url_create.slug
