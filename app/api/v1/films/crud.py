import logging
from redis import Redis
from pydantic import BaseModel, ValidationError

from core import FILM_DIR
from core import config
from schemas import Films, FilmsCreate, FilmsUpdate, FilmsParticularUpdate

log = logging.getLogger(__name__)


redis_storage = Redis(
    port=config.REDIS_PORT,
    host=config.REDIS_HOST,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmStorage(BaseModel):
    slug_to_item: dict[str, Films] = {}

    def save(self):
        FILM_DIR.write_text(self.model_dump_json(indent=2))
        log.info("Saved films to storage file")

    @classmethod
    def load(cls) -> "FilmStorage":
        if not FILM_DIR.exists():
            log.info("Fils directory does not exist")
            return FilmStorage()
        return cls.model_validate_json(FILM_DIR.read_text())

    def init_storage_from_state(self):
        try:
            data = FilmStorage.load()
        except ValidationError:
            self.save()
            log.warning("Rewritten films storage file")
        film_storage.slug_to_item.update(data.slug_to_item)
        self.save()
        log.warning("Recovered data from films file")

    def get(self) -> list[Films]:
        return list(self.slug_to_item.values())

    def get_by_slug(self, slug: str) -> Films | None:
        data = redis_storage.hget(
            name=config.REDIS_TOKENS_FILMS_HASH_NAME,
            key=slug,
        )
        return Films.model_validate_json(data) if data else None

    def create(self, data: FilmsCreate) -> Films:
        new_film = Films(**data.model_dump())
        redis_storage.hset(
            name=config.REDIS_TOKENS_FILMS_HASH_NAME,
            key=new_film.slug,
            value=new_film.model_dump_json(),
        )
        log.info("Created new film %s", new_film)
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_item.pop(slug, None)

    def delete(self, film: Films) -> None:
        self.delete_by_slug(film.slug)

    def update(self, film: Films, film_in: FilmsUpdate) -> Films:
        for key, value in film_in:
            setattr(film, key, value)
        return film

    def particular_update(self, film: Films, film_in: FilmsParticularUpdate) -> Films:
        for key, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, key, value)
        return film


film_storage = FilmStorage()
