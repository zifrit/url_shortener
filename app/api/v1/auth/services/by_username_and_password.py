import secrets
from abc import ABC, abstractmethod

from redis import Redis

from core import config


class ABCUsersStorage(ABC):

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        Find password from redis DB or det None
        :param username: user username
        :return: password or None
        """

    @classmethod
    def check_password(cls, password1: str, password2: str) -> bool:
        """
        :param password1:
        :param password2:
        :return:
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str) -> bool:
        """
        :param username: user username
        :param password: checking password
        :return: True if password is valid, False otherwise
        """

        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_password(password, db_password)


class RedisUserstorage(ABCUsersStorage):

    def __init__(
        self,
        host: str = config.REDIS_HOST,
        port: int = config.REDIS_PORT,
        db: int = config.REDIS_DB_USERS,
    ):
        self.redis_client = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get_user_password(self, username: str) -> str | None:
        return self.redis_client.get(username)


cache_user_storage = RedisUserstorage()
