import logging
from redis import Redis
from pydantic import BaseModel, ValidationError, HttpUrl

from core import config
from schemas import ShortUrl, ShortUrlCreate, ShortUrlUpdate, ShortUrlParticularUpdate

log = logging.getLogger(__name__)


redis_storage = Redis(
    port=config.REDIS_PORT,
    host=config.REDIS_HOST,
    db=config.REDIS_DB_SHORT_URL,
    decode_responses=True,
)


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
        datas = redis_storage.hvals(
            name=config.REDIS_TOKENS_SHORT_URL_HASH_NAME,
        )
        return (
            [ShortUrl.model_validate_json(short_url) for short_url in datas]
            if datas
            else []
        )

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        data = redis_storage.hget(
            name=config.REDIS_TOKENS_SHORT_URL_HASH_NAME,
            key=slug,
        )
        return ShortUrl.model_validate_json(data) if data else None

    def create(self, data: ShortUrlCreate) -> ShortUrl:
        new_short_url = ShortUrl(**data.model_dump())
        log.info("Created new short url %s", new_short_url)
        self.save_to_redis_storage(new_short_url)
        return new_short_url

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
