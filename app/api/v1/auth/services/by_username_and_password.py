from abc import ABC, abstractmethod
from typing import cast

from redis import Redis

from core import config


class ABCUsersStorage(ABC):

    @abstractmethod
    def get_user_password(self, username: str) -> str | None:
        """
        Find password from redis DB or get None
        :param username: user username
        :return: password or None
        """

    @abstractmethod
    def add_user(self, username: str, password: str) -> str | None:
        """
        Add user to storage
        :param username: user username
        :param password: user password
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
        host: str = config.settings.redis.connection.host,
        port: int = config.settings.redis.connection.port,
        db: int = config.settings.redis.db.db_users,
    ) -> None:
        self.redis_client = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get_user_password(self, username: str) -> str | None:
        return cast(
            str | None,
            self.redis_client.get(username),
        )

    def add_user(self, username: str, password: str) -> str | None:
        if self.get_user_password(username) is not None:
            return None
        self.redis_client.set(username, password)
        return password


cache_user_storage = RedisUserstorage()
