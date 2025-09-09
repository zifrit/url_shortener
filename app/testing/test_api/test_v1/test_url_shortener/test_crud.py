import random
import string
from os import getenv
from unittest import TestCase

from pydantic import HttpUrl

from api.v1.url_shortener.crud import storage
from schemas import ShortUrl, ShortUrlCreate, ShortUrlParticularUpdate, ShortUrlUpdate

if getenv("TESTING") != "1":
    raise OSError(  # noqa: TRY003
        "Environmental is not ready to start test",  # noqa: EM101
    )


class ShortUrlStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.short_url = self.create_short_ulr()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def create_short_ulr(self) -> ShortUrl:
        short_url_in = ShortUrlCreate(
            slug="".join(random.choices(string.ascii_letters, k=8)),
            description="some-description",
            target_url="https://example.com",
        )
        return storage.create(short_url_in)

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
