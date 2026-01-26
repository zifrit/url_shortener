from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from storage.short_ulr.crud import storage
from main import app
from schemas import ShortUrl, ShortUrlUpdate
from testing.test_api.conftest import create_short_url


class TestUpdate:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        slug, description, target_url = request.param
        short_url = create_short_url(
            target_url=target_url,
            description=description,
            slug=slug,
        )
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description, new_target_url",
        [
            pytest.param(
                ("new_slug_1", "description", "https://example.com/"),
                "new_description",
                "https://new-example.com/",
                id="new_slug_1",
            ),
            pytest.param(
                ("new_slug_2", "", "https://google.com/"),
                "new_description",
                "https://example.com/",
                id="new_slug_2",
            ),
            pytest.param(
                ("new_slug_3", "description", "http://ya.com/"),
                "",
                "http://new.com/",
                id="new_slug_3",
            ),
        ],
        indirect=["short_url"],
    )
    def test_update_short_url(
        self,
        short_url: ShortUrl,
        new_description: str,
        new_target_url: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for("update_short_url_details", slug=short_url.slug)
        data = ShortUrlUpdate(
            description=new_description,
            target_url=new_target_url,
        )
        old_description = short_url.description
        old_target_url = short_url.target_url
        response = auth_client.put(url, json=data.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK, response.text
        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        assert short_url_db.description == new_description
        assert str(short_url_db.target_url) == new_target_url
        assert old_description != new_description
        assert str(old_target_url) != new_target_url
