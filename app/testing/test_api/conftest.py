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


def build_short_url_create(
    slug: str,
    description: str = "some-description",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=slug,
        description=description,
        target_url="https://example.com",
    )


def build_short_url_random_slug() -> ShortUrlCreate:
    return ShortUrlCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),  # noqa: S311
        description="some-description",
        target_url="https://example.com",
    )


def create_short_url_random_slug() -> ShortUrl:
    short_url_in = build_short_url_random_slug()
    return storage.create(short_url_in)


def create_short_url(
    slug: str,
    description: str = "some-description",
) -> ShortUrl:
    short_url_in = build_short_url_create(slug, description)
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url_random_slug()
    yield short_url
    storage.delete(short_url)


def build_movie_create_random_slug() -> FilmsCreate:
    return FilmsCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),  # noqa: S311
        name="some-name",
        description="some-description",
        author="some-author",
    )


def build_movie_create(
    slug: str,
    description: str = "some-description",
) -> FilmsCreate:
    return FilmsCreate(
        slug=slug,
        name="some-name",
        description=description,
        author="some-author",
    )


def create_films_random_slug() -> Films:
    film_in = build_movie_create_random_slug()
    return film_storage.create(film_in)


def create_films(
    slug: str,
    description: str = "some-description",
) -> Films:
    film_in = build_movie_create(slug, description)
    return film_storage.create(film_in)


@pytest.fixture()
def film() -> Generator[Films]:
    film = create_films_random_slug()
    yield film
    film_storage.delete(film)
