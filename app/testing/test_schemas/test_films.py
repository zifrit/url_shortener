from os import getenv
from unittest import TestCase

import pytest
from pydantic import ValidationError

from schemas.films import Films, FilmsCreate, FilmsParticularUpdate, FilmsUpdate

if getenv("TESTING") != "1":
    pytest.exit("Environmental is not ready to start test")


class FilmsTestCase(TestCase):
    def test_film_create_can_be_created_from_create_schemas(self) -> None:
        film_create = FilmsCreate(
            slug="some-slug",
            name="some-name",
            description="some-description",
            author="some-author",
        )
        film = Films(**film_create.model_dump())

        self.assertEqual(
            film.slug,
            film_create.slug,
        )

        self.assertEqual(
            film.name,
            film_create.name,
        )

        self.assertEqual(
            film.description,
            film_create.description,
        )

        self.assertEqual(
            film.author,
            film_create.author,
        )

    def test_update_film_from_film_schema(self) -> None:
        film = Films(
            slug="some-slug",
            name="some-name",
            description="some-description",
            author="some-author",
        )
        updated_film = FilmsUpdate(
            name="new-some-name",
            description="new-some-description",
            author="new-some-author",
        )
        for key, value in updated_film:
            setattr(film, key, value)

        self.assertEqual(
            film.name,
            updated_film.name,
        )

        self.assertEqual(
            film.description,
            updated_film.description,
        )

        self.assertEqual(
            film.author,
            updated_film.author,
        )

    def test_film_can_be_particular_update_from_film_schema(self) -> None:
        film = Films(
            slug="some-slug",
            name="some-name",
            description="some-description",
            author="some-author",
        )

        particular_film = FilmsParticularUpdate(
            name="new-some-name",
        )

        for key, value in particular_film.model_dump(exclude_unset=True).items():
            setattr(film, key, value)

        self.assertEqual(
            film.name,
            particular_film.name,
        )

        self.assertEqual(
            "some-author",
            film.author,
        )

        self.assertEqual(
            "some-description",
            film.description,
        )

        film = Films(
            slug="some-slug",
            name="some-name",
            description="some-description",
            author="some-author",
        )

        particular_film = FilmsParticularUpdate()

        for key, value in particular_film.model_dump(exclude_unset=True).items():
            setattr(film, key, value)

        self.assertEqual(
            "some-name",
            film.name,
        )

        self.assertEqual(
            "some-author",
            film.author,
        )

        self.assertEqual(
            "some-description",
            film.description,
        )

    def test_film_url_create_accepts_different_data(self) -> None:
        datas = [
            (
                "some-new-slug-1",
                "some-new-name-1",
                "some-new-author-1",
            ),
            (
                "some-new-slug-2",
                "some-new-name-2",
                "some-new-author-2",
            ),
            (
                "some-new-slug-2",
                "some-new-name-2",
                "some-new-author-2",
            ),
        ]
        for slug, name, author in datas:
            with self.subTest(
                slug=slug,
                name=name,
                author=author,
                msg="test-create-film",
            ):
                film = Films(
                    slug=slug,
                    name=name,
                    description="some-description",
                    author=author,
                )
                self.assertEqual(film.slug, slug)
                self.assertEqual(film.name, name)
                self.assertEqual(film.author, author)

    def test_short_url_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            FilmsCreate(
                slug="s",
                name="some-name",
                description="some-description",
                author="some-author",
            )
        error_details = exc_info.exception.errors()[0]
        expect_type = "string_too_short"
        self.assertEqual(
            expect_type,
            error_details["type"],
        )

    def test_short_url_slug_too_shore_regx(self) -> None:
        with self.assertRaisesRegex(
            ValidationError,
            "String should have at least 3 characters",
        ):
            FilmsCreate(
                slug="s",
                name="some-name",
                description="some-description",
                author="some-author",
            )
