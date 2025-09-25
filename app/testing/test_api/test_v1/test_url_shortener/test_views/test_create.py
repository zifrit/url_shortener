import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas import ShortUrl, ShortUrlCreate


def test_create_short_ulr(auth_client: TestClient) -> None:
    url = app.url_path_for("create_short_url")
    data = ShortUrlCreate(
        slug="".join(random.choices(string.ascii_letters, k=10)),  # noqa: S311
        description="some-description",
        target_url="https://example.com",
    ).model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert response_data["slug"] == data["slug"]
    assert ShortUrl(**response_data) == ShortUrl(**data)


def test_create_short_ulr_already_exist(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    url = app.url_path_for("create_short_url")
    data = ShortUrlCreate(**short_url.model_dump()).model_dump(mode="json")
    auth_client.post(url=url, json=data)
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (
        response_data["detail"]
        == f"Short URL with this slug='{data["slug"]}' already exists"
    )
