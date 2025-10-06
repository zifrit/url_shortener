import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app


@pytest.mark.xfail(raises=NotImplementedError, reason="test failed api method")
def test_failed_api(
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "failed_api",
        slug="non_existent_slug",
    )
    auth_response = auth_client.post(url)
    assert auth_response.status_code == status.HTTP_200_OK
