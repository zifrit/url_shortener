from typing import ClassVar
from unittest import TestCase

import pytest

from api.v1.films.crud import AlreadyExistFilmError, film_storage
from schemas import Films, FilmsCreate, FilmsParticularUpdate, FilmsUpdate
from testing.test_api.conftest import create_films_random_slug


class FilmStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.film = create_films_random_slug()

    def tearDown(self) -> None:
        film_storage.delete(self.film)

    def test_update(self) -> None:
        film_update = FilmsUpdate(
            **self.film.model_dump(),
        )
        source_description = self.film.description
        source_name = self.film.name
        source_author = self.film.author

        film_update.description = self.film.description * 2
        film_update.name = self.film.name * 2
        film_update.author = (
            self.film.author * 2 if self.film.author else self.film.author
        )
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


class FilmStorageGetTestCase(TestCase):
    FILMS_COUNT = 3
    films: ClassVar[list[Films]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.films = [create_films_random_slug() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for film in cls.films:
            film_storage.delete(film)

    def test_get_list(self) -> None:
        films = film_storage.get()
        slugs = {su.slug for su in films}
        expected_slugs = {su.slug for su in self.films}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(
                slug=film.slug,
                msg=f"Validate can get slug {film.slug}",
            ):
                db_film = film_storage.get_by_slug(film.slug)
                self.assertEqual(
                    film,
                    db_film,
                )


def test_create_or_raise_if_exists(film: Films) -> None:
    film_create = FilmsCreate(**film.model_dump())
    with pytest.raises(
        AlreadyExistFilmError,
        match=film_create.slug,
    ) as exc_ingo:
        film_storage.create_or_raise_if_exists(film_create)

    assert exc_ingo.value.args[0] == film_create.slug
