import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.v1.films.crud import film_storage
from main import app
from schemas import Films, FilmsCreate


def create_film(slug: str) -> Films:
    film_in = FilmsCreate(
        slug=slug,
        name="some-name",
        description="some-description",
        author="some-author",
    )
    return film_storage.create(film_in)


@pytest.fixture(
    params=[
        "some-slug",
        "some",
        pytest.param("slu", id="min_length"),
        pytest.param("slugslugsl", id="max_length"),
    ],
)
def film(request: SubRequest) -> Films:
    return create_film(request.param)


def test_delete_film(
    auth_client: TestClient,
    film: Films,
) -> None:
    url = app.url_path_for(
        "delete_film",
        slug=film.slug,
    )
    auth_response = auth_client.delete(url)
    assert auth_response.status_code == status.HTTP_204_NO_CONTENT
    assert not film_storage.exists(film.slug)
