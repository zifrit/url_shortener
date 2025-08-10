from pydantic import BaseModel
from schemas import Films, FilmsCreate


class FilmStorage(BaseModel):
    slug_to_film: dict[str, Films] = {}

    def get(self) -> list[Films]:
        return list(self.slug_to_film.values())

    def get_by_slug(self, slug: str) -> Films | None:
        return self.slug_to_film.get(slug)

    def create(self, data: FilmsCreate) -> Films:
        new_film = Films(**data.model_dump())
        self.slug_to_film[new_film.slug] = new_film
        return new_film


fim_storage = FilmStorage()

fim_storage.create(
    FilmsCreate(
        slug="avatar",
        name="Avatar",
        description="First amazing film",
        author="James Francis Cameron",
    ),
)
fim_storage.create(
    FilmsCreate(
        slug="avatar_2",
        name="Avatar2",
        description="Second amazing film",
        author="James Francis Cameron",
    ),
)
fim_storage.create(
    FilmsCreate(
        slug="avatar_3",
        name="Avatar3",
        description="Third amazing film",
        author="James Francis Cameron",
    ),
)
