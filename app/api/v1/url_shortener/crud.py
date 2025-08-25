__all__ = "storage"

import logging
from typing import cast

from app.core import config
from app.schemas import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlParticularUpdate,
    ShortUrlUpdate,
)
from pydantic import BaseModel
from redis import Redis

log = logging.getLogger(__name__)


redis_storage = Redis(
    port=config.REDIS_PORT,
    host=config.REDIS_HOST,
    db=config.REDIS_DB_SHORT_URL,
    decode_responses=True,
)


class BaseShortUrlError(Exception):
    """
    Base exception for short url error
    """


class AlreadyExistsShortUrlError(BaseShortUrlError):
    """
    Short url already exists error
    """


class ShortUrlStorage(BaseModel):
    slug_to_item: dict[str, ShortUrl] = {}

    @classmethod
    def save_to_redis_storage(cls, short_url: ShortUrl) -> None:
        redis_storage.hset(
            name=config.REDIS_TOKENS_SHORT_URL_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self) -> list[ShortUrl]:
        datas = cast(
            list[str],
            redis_storage.hvals(
                name=config.REDIS_TOKENS_SHORT_URL_HASH_NAME,
            ),
        )
        return (
            [ShortUrl.model_validate_json(short_url) for short_url in datas]
            if datas
            else []
        )

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        data = cast(
            str,
            redis_storage.hget(
                name=config.REDIS_TOKENS_SHORT_URL_HASH_NAME,
                key=slug,
            ),
        )
        return ShortUrl.model_validate_json(data) if data else None

    def create(self, data: ShortUrlCreate) -> ShortUrl:
        new_short_url = ShortUrl(**data.model_dump())
        log.info("Created new short url %s", new_short_url)
        self.save_to_redis_storage(new_short_url)
        return new_short_url

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis_storage.hexists(
                name=config.REDIS_TOKENS_SHORT_URL_HASH_NAME,
                key=slug,
            ),
        )

    def create_or_raise_if_exists(
        self, short_url: ShortUrlCreate
    ) -> ShortUrl | AlreadyExistsShortUrlError:
        if not self.exists(short_url.slug):
            return self.create(short_url)
        raise AlreadyExistsShortUrlError(short_url.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis_storage.hdel(config.REDIS_TOKENS_SHORT_URL_HASH_NAME, slug)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(short_url.slug)

    def update(self, short_url: ShortUrl, short_url_in: ShortUrlUpdate) -> ShortUrl:
        for key, value in short_url_in:
            setattr(short_url, key, value)
        self.save_to_redis_storage(short_url)
        return short_url

    def particular_update(
        self, short_url: ShortUrl, short_url_in: ShortUrlParticularUpdate
    ) -> ShortUrl:
        for key, value in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, key, value)
        self.save_to_redis_storage(short_url)
        return short_url


storage = ShortUrlStorage()
