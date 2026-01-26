import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from storage.short_ulr.crud import storage
from main import app
from schemas import ShortUrl
from testing.test_api.conftest import create_short_url


@pytest.fixture(
    params=[
        "some-slug",
        "slug",
        pytest.param("som", id="min_length"),
        pytest.param("somsomsoms", id="max_length"),
    ],
)
def short_url(request: SubRequest) -> ShortUrl:
    return create_short_url(request.param)


def test_delete_short_url(
    auth_client: TestClient,
    short_url: ShortUrl,
) -> None:
    url = app.url_path_for(
        "delete_short_url",
        slug=short_url.slug,
    )
    auth_response = auth_client.delete(url)
    assert auth_response.status_code == status.HTTP_204_NO_CONTENT
    assert not storage.exists(short_url.slug)
