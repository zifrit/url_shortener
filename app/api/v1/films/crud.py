__all__ = "film_storage"

import logging
from typing import cast

from app.core import config
from app.schemas import Films, FilmsCreate, FilmsParticularUpdate, FilmsUpdate
from pydantic import BaseModel
from redis import Redis

log = logging.getLogger(__name__)


redis_storage = Redis(
    port=config.REDIS_PORT,
    host=config.REDIS_HOST,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmError(Exception):
    """
    Film related error
    """


class AlreadyExistFilmError(FilmError):
    """
    Film already exists error
    """


class FilmStorage(BaseModel):
    slug_to_item: dict[str, Films] = {}

    @classmethod
    def save_to_redis_storage(cls, film: Films) -> None:
        redis_storage.hset(
            name=config.REDIS_TOKENS_FILMS_HASH_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )

    def get(self) -> list[Films]:
        datas = cast(
            list[str],
            redis_storage.hvals(
                name=config.REDIS_TOKENS_FILMS_HASH_NAME,
            ),
        )
        return [Films.model_validate_json(film) for film in datas] if datas else []

    def get_by_slug(self, slug: str) -> Films | None:
        data = cast(
            str,
            redis_storage.hget(
                name=config.REDIS_TOKENS_FILMS_HASH_NAME,
                key=slug,
            ),
        )
        return Films.model_validate_json(data) if data else None

    def create(self, data: FilmsCreate) -> Films:
        new_film = Films(**data.model_dump())
        log.info("Created new film %s", new_film)
        self.save_to_redis_storage(new_film)
        return new_film

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis_storage.hexists(
                name=config.REDIS_TOKENS_FILMS_HASH_NAME,
                key=slug,
            ),
        )

    def create_or_raise_if_exists(
        self, film: FilmsCreate
    ) -> Films | AlreadyExistFilmError:
        if not self.exists(film.slug):
            return self.create(film)
        raise AlreadyExistFilmError(film.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis_storage.hdel(config.REDIS_TOKENS_FILMS_HASH_NAME, slug)

    def delete(self, film: Films) -> None:
        self.delete_by_slug(film.slug)

    def update(self, film: Films, film_in: FilmsUpdate) -> Films:
        for key, value in film_in:
            setattr(film, key, value)
        self.save_to_redis_storage(film)
        return film

    def particular_update(self, film: Films, film_in: FilmsParticularUpdate) -> Films:
        for key, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, key, value)
        self.save_to_redis_storage(film)
        return film


film_storage = FilmStorage()
