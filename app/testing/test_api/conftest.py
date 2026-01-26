import random
import string
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from api.v1.auth.services.by_token import cache_token_storage
from storage.film.crud import film_storage
from storage.short_ulr.crud import storage
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
    target_url: str = "https://example.com",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug=slug,
        description=description,
        target_url=target_url,
    )


def build_short_url_random_slug(
    description: str = "some-description",
    target_url: str = "https://example.com",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),
        description=description,
        target_url=target_url,
    )


def create_short_url_random_slug(
    description: str = "some-description",
    target_url: str = "https://example.com",
) -> ShortUrl:
    short_url_in = build_short_url_random_slug(description, target_url)
    return storage.create(short_url_in)


def create_short_url(
    slug: str,
    description: str = "some-description",
    target_url: str = "https://example.com",
) -> ShortUrl:
    short_url_in = build_short_url_create(slug, description, target_url)
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url_random_slug()
    yield short_url
    storage.delete(short_url)


def build_movie_create_random_slug(
    description: str = "some-description",
    name: str = "some-name",
    author: str = "some-author",
) -> FilmsCreate:
    return FilmsCreate(
        slug="".join(random.choices(string.ascii_letters, k=8)),
        name=name,
        description=description,
        author=author,
    )


def build_movie_create(
    slug: str,
    description: str = "some-description",
    name: str = "some-name",
    author: str = "some-author",
) -> FilmsCreate:
    return FilmsCreate(
        slug=slug,
        name=name,
        description=description,
        author=author,
    )


def create_films_random_slug(
    description: str = "some-description",
    name: str = "some-name",
    author: str = "some-author",
) -> Films:
    film_in = build_movie_create_random_slug(description, name, author)
    return film_storage.create(film_in)


def create_films(
    slug: str,
    description: str = "some-description",
    name: str = "some-name",
    author: str = "some-author",
) -> Films:
    film_in = build_movie_create(slug, description, name, author)
    return film_storage.create(film_in)


@pytest.fixture()
def film() -> Generator[Films]:
    film = create_films_random_slug()
    yield film
    film_storage.delete(film)
