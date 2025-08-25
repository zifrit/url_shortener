__all__ = "cache_token_storage"

import secrets
from abc import ABC, abstractmethod
from typing import cast

from app.core import config
from redis import Redis


class ABCTokenRedisStorage(ABC):

    @abstractmethod
    def token_exists(self, token: str) -> bool:
        """
        Check if a token exists.
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Save token in storage.
        :param token:
        :return:
        """

    @abstractmethod
    def gel_all(self) -> list[str]:
        """
        Get all tokens.
        :return:
        """

    @abstractmethod
    def rm_token(self, token: str) -> None:
        """
        Remove token from storage.
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(20)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokenStorage(ABCTokenRedisStorage):

    def __init__(
        self,
        host: str = config.REDIS_HOST,
        port: int = config.REDIS_PORT,
        db: int = config.REDIS_DB_TOKENS,
        token_set_name: str = config.REDIS_TOKENS_SET_NAME,
    ) -> None:
        self.redis_client = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.token_set_name = token_set_name

    def token_exists(self, token: str) -> bool:
        return bool(
            self.redis_client.sismember(
                self.token_set_name,
                token,
            ),
        )

    def add_token(self, token: str) -> None:
        self.redis_client.sadd(
            self.token_set_name,
            token,
        )

    def gel_all(self) -> list[str]:
        return list(
            cast(
                set[str],
                self.redis_client.smembers(
                    name=self.token_set_name,
                ),
            )
        )

    def rm_token(self, token: str) -> None:
        self.redis_client.srem(
            self.token_set_name,
            token,
        )


cache_token_storage = RedisTokenStorage()
