import logging
import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas import Films, FilmsCreate
from testing.test_api.conftest import create_films_random_slug


@pytest.mark.apitest
def test_create_film(
    caplog: pytest.LogCaptureFixture,
    auth_client: TestClient,
) -> None:
    caplog.set_level(logging.INFO)
    url = app.url_path_for("create_film")
    data = FilmsCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),
        name="some-name",
        description="some-description",
        author="some-author",
    ).model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert FilmsCreate(**response_data) == FilmsCreate(**data)
    assert "Created new film" in caplog.text
    assert response_data["slug"] in caplog.text


@pytest.mark.apitest
def test_create_film_already_exists(auth_client: TestClient, film: Films) -> None:
    url = app.url_path_for("create_film")
    data = FilmsCreate(**film.model_dump()).model_dump(mode="json")
    auth_client.post(url=url, json=data)
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (
        response_data["detail"]
        == f"Film with this slug='{data["slug"]}' already exists"
    )


@pytest.mark.apitest
class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("s", "string_too_short"), id="short_Slug"),
            pytest.param(("some-long-slug-text", "string_too_long"), id="short_Slug"),
        ],
    )
    def films_create_values(self, request: SubRequest) -> tuple[dict[str, Any], str]:
        build = create_films_random_slug()
        data = build.model_dump(mode="json")
        slug, error = request.param
        data["slug"] = slug
        return data, error

    def test_invalid_slug(
        self,
        films_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_film")
        create_data, error = films_create_values
        response = auth_client.post(url=url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_details = response.json()["detail"][0]
        assert error_details["type"] == error
