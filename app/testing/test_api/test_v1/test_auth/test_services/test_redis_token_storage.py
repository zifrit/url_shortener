from unittest import TestCase

from services.auth.by_token import cache_token_storage


class RedisTokenStorageTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        token = cache_token_storage.generate_and_save_token()
        self.assertTrue(
            cache_token_storage.token_exists(token),
        )
