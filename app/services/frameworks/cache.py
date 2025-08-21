import secrets
from abc import ABC, abstractmethod

from redis import Redis
from core import config


class ABCTokenCache(ABC):

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

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(20)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokenCache(ABCTokenCache):

    def __init__(
        self,
        host: str = config.REDIS_HOST,
        port: int = config.REDIS_PORT,
        db: int = config.REDIS_DB_TOKENS,
        token_set_name: str = config.REDIS_TOKENS_SET_NAME,
    ):
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


cache_token_storage = RedisTokenCache()
