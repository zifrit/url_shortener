import random
import string
from os import getenv
from unittest import TestCase

from api.v1.films.crud import film_storage
from schemas import Films, FilmsCreate, FilmsParticularUpdate, FilmsUpdate

if getenv("TESTING") != "1":
    raise OSError(  # noqa: TRY003
        "Environmental is not ready to start test",  # noqa: EM101
    )


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = self.create_short_ulr()

    def tearDown(self) -> None:
        film_storage.delete(self.film)

    def create_short_ulr(self) -> Films:
        short_url_in = FilmsCreate(
            slug="".join(random.choices(string.ascii_letters, k=8)),
            name="some-name",
            description="some-description",
            author="some-author",
        )
        return film_storage.create(short_url_in)

    def test_update(self) -> None:
        film_update = FilmsUpdate(
            **self.film.model_dump(),
        )
        source_description = self.film.description
        source_name = self.film.name
        source_author = self.film.author

        film_update.description = self.film.description * 2
        film_update.name = self.film.name * 2
        film_update.author = self.film.author * 2
        updated_film = film_storage.update(
            film=self.film,
            film_in=film_update,
        )
        self.assertNotEqual(
            source_description,
            updated_film.description,
        )
        self.assertNotEqual(
            source_name,
            updated_film.name,
        )
        self.assertNotEqual(
            source_author,
            updated_film.author,
        )
        self.assertEqual(
            film_update,
            FilmsUpdate(**updated_film.model_dump()),
        )

    def test_particular_update(self) -> None:
        film_particular_update = FilmsParticularUpdate(
            description=self.film.description * 2,
        )
        source_description = self.film.description
        updated_film = film_storage.particular_update(
            film=self.film,
            film_in=film_particular_update,
        )

        self.assertNotEqual(
            source_description,
            updated_film.description,
        )
        self.assertEqual(
            film_particular_update.description,
            updated_film.description,
        )
