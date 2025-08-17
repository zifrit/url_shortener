from pydantic import BaseModel, ValidationError

from core import FILM_DIR
from schemas import Films, FilmsCreate, FilmsUpdate, FilmsParticularUpdate


class FilmStorage(BaseModel):
    slug_to_item: dict[str, Films] = {}

    def save(self):
        FILM_DIR.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls) -> "FilmStorage":
        if not FILM_DIR.exists():
            return FilmStorage()
        return cls.model_validate_json(FILM_DIR.read_text())

    def get(self) -> list[Films]:
        return list(self.slug_to_item.values())

    def get_by_slug(self, slug: str) -> Films | None:
        return self.slug_to_item.get(slug)

    def create(self, data: FilmsCreate) -> Films:
        new_film = Films(**data.model_dump())
        self.slug_to_item[new_film.slug] = new_film
        self.save()
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.save()
        self.slug_to_item.pop(slug, None)

    def delete(self, film: Films) -> None:
        self.delete_by_slug(film.slug)

    def update(self, film: Films, film_in: FilmsUpdate) -> Films:
        for key, value in film_in:
            setattr(film, key, value)
        self.save()
        return film

    def particular_update(self, film: Films, film_in: FilmsParticularUpdate) -> Films:
        for key, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, key, value)
        self.save()
        return film


try:
    film_storage = FilmStorage.load()
except ValidationError:
    film_storage = FilmStorage()
    film_storage.create(
        FilmsCreate(
            slug="avatar",
            name="Avatar",
            description="First amazing film",
            author="James Francis Cameron",
        ),
    )
    film_storage.create(
        FilmsCreate(
            slug="avatar_2",
            name="Avatar2",
            description="Second amazing film",
            author="James Francis Cameron",
        ),
    )
    film_storage.create(
        FilmsCreate(
            slug="avatar_3",
            name="Avatar3",
            description="Third amazing film",
            author="James Francis Cameron",
        ),
    )
