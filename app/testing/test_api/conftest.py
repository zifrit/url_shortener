import random
import string
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.v1.auth.services.by_token import cache_token_storage
from api.v1.films.crud import film_storage
from api.v1.url_shortener.crud import storage
from main import app
from schemas import Films, FilmsCreate, ShortUrl, ShortUrlCreate


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = cache_token_storage.generate_and_save_token()
    yield token
    cache_token_storage.rm_token(token)


@pytest.fixture(scope="module")
def auth_client(client: TestClient, auth_token: str) -> TestClient:
    client.headers.update({"Authorization": f"Bearer {auth_token}"})
    return client


def create_short_url() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),  # noqa: S311
        description="some-description",
        target_url="https://example.com",
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url()
    yield short_url
    storage.delete(short_url)


def create_film() -> Films:
    film_in = FilmsCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),  # noqa: S311
        name="some-name",
        description="some-description",
        author="some-author",
    )
    return film_storage.create(film_in)


@pytest.fixture()
def film() -> Generator[Films]:
    film = create_film()
    yield film
    film_storage.delete(film)
