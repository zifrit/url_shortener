from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas import Films, FilmsUpdate
from storage.film.crud import film_storage
from testing.test_api.conftest import create_films_random_slug


@pytest.mark.apitest
class TestUpdate:

    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[Films]:
        description, name, author = request.param
        film = create_films_random_slug(
            description=description,
            name=name,
            author=author,
        )
        yield film
        film_storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description, new_name, new_author",
        [
            pytest.param(
                ("description", "name", "author"),
                "new_description",
                "new_name",
                "new_author",
                id="standard",
            ),
            pytest.param(
                ("description", "name", "author"),
                "new_description",
                "n",
                "new_author",
                id="standard",
            ),
            pytest.param(
                ("description", "name", "author"),
                "new_description",
                "new_name",
                "",
                id="standard",
            ),
        ],
        indirect=["film"],
    )
    def test_update_film_details(
        self,
        film: Films,
        new_description: str,
        new_name: str,
        new_author: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_film_details",
            slug=film.slug,
        )
        data = FilmsUpdate(
            description=new_description,
            name=new_name,
            author=new_author,
        )
        old_description = film.description
        old_name = film.name
        old_author = film.author
        response = auth_client.patch(url, json=data.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = film_storage.get_by_slug(film.slug)
        assert film_db
        assert old_description != new_description
        assert film_db.description == new_description
        assert old_name != new_name
        assert film_db.name == new_name
        assert old_author != new_author
        assert film_db.author == new_author
