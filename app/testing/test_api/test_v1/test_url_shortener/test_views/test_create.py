import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas import ShortUrl, ShortUrlCreate
from testing.test_api.conftest import create_short_url_random_slug


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


class TestCreateInvalid:

    @pytest.fixture(
        params=[
            pytest.param(("s", "string_too_short"), id="short_Slug"),
            pytest.param(("some-long-slug-text", "string_too_long"), id="short_Slug"),
        ],
    )
    def short_url_create_values(
        self,
        request: SubRequest,
    ) -> tuple[dict[str, Any], str]:
        build = create_short_url_random_slug()
        data = build.model_dump(mode="json")
        slug, error = request.param
        data["slug"] = slug
        return data, error

    def test_invalid_slug(
        self,
        short_url_create_values: tuple[dict[str, Any], str],
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("create_short_url")
        create_data, error = short_url_create_values
        response = auth_client.post(url=url, json=create_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_details = response.json()["detail"][0]
        assert error_details["type"] == error
