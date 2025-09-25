import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas import Films, FilmsCreate


def test_create_film(auth_client: TestClient) -> None:
    url = app.url_path_for("create_film")
    data = FilmsCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),  # noqa: S311
        name="some-name",
        description="some-description",
        author="some-author",
    ).model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert FilmsCreate(**response_data) == FilmsCreate(**data)


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
