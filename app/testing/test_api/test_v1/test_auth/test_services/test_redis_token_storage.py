from os import getenv
from unittest import TestCase

import pytest

from api.v1.auth.services.by_token import cache_token_storage

if getenv("TESTING") != "1":
    pytest.exit("Environmental is not ready to start test")


class RedisTokenStorageTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        token = cache_token_storage.generate_and_save_token()
        self.assertTrue(
            cache_token_storage.token_exists(token),
        )
