from fastapi import status
from fastapi.testclient import TestClient


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "home.html"  # type: ignore[attr-defined]
    assert "features" in response.context  # type: ignore[attr-defined]
