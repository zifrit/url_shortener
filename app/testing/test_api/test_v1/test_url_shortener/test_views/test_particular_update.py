from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from core.config import DESCRIPTION_MAX_LENGTH
from main import app
from schemas import ShortUrl
from storage.short_ulr.crud import storage
from testing.test_api.conftest import create_short_url


class TestUpdateParticular:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        slug, description = request.param
        short_url = create_short_url(slug, description)
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description",
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
        indirect=["short_url"],
    )
    def test_particular_update_short_url_details(
        self,
        short_url: ShortUrl,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "particular_update_short_url_details",
            slug=short_url.slug,
        )
        data = {"description": new_description}
        old_description = short_url.description
        response = auth_client.patch(url, json=data)
        assert response.status_code == status.HTTP_200_OK, response.text
        short_url_db = storage.get_by_slug(short_url.slug)
        assert short_url_db
        assert old_description != new_description
        assert short_url_db.description == new_description
