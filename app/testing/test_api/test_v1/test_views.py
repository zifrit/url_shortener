import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "home.html"
    assert "features" in response.context
