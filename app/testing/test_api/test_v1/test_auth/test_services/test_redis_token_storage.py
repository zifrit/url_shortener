from os import getenv
from unittest import TestCase

from api.v1.auth.services.by_token import cache_token_storage

if getenv("TESTING") != "1":
    raise OSError(  # noqa: TRY003
        "Environmental is not ready to start test",  # noqa: EM101
    )


class RedisTokenStorageTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        token = cache_token_storage.generate_and_save_token()
        self.assertTrue(
            cache_token_storage.token_exists(token),
        )
