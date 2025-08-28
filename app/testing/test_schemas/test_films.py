from unittest import TestCase

from schemas.films import Films, FilmsCreate


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
        updated_film = Films(
            slug="new-some-slug",
            name="new-some-name",
            description="new-some-description",
            author="new-some-author",
        )
        for key, value in updated_film:
            setattr(film, key, value)

        self.assertEqual(
            film.slug,
            updated_film.slug,
        )

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
