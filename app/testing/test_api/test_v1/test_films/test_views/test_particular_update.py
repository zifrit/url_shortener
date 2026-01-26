from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from storage.film.crud import film_storage
from core.config import DESCRIPTION_MAX_LENGTH
from main import app
from schemas import Films
from testing.test_api.conftest import create_films


class TestUpdateParticular:

    @pytest.fixture()
    def film(self, request: SubRequest) -> Generator[Films]:
        slug, description = request.param
        film = create_films(slug, description)
        yield film
        film_storage.delete(film)

    @pytest.mark.parametrize(
        "film, new_description",
        [
            pytest.param(
                ("foo", "a description"),
                "",
                id="with description",
            ),
            pytest.param(
                ("bar", ""),
                "some_description",
                id="without description",
            ),
            pytest.param(
                ("bar", "a" * DESCRIPTION_MAX_LENGTH),
                "",
                id="min length description",
            ),
            pytest.param(
                ("bar", ""),
                "a" * DESCRIPTION_MAX_LENGTH,
                id="max length description",
            ),
        ],
        indirect=["film"],
    )
    def test_particular_update_film_details(
        self,
        film: Films,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "particular_update_film_details",
            slug=film.slug,
        )
        data = {"description": new_description}
        old_description = film.description
        response = auth_client.patch(url, json=data)
        assert response.status_code == status.HTTP_200_OK, response.text
        film_db = film_storage.get_by_slug(film.slug)
        assert film_db
        assert old_description != new_description
        assert film_db.description == new_description
