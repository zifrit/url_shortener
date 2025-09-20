from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_view() -> None:
    name = "Jone"
    params = {"name": name}
    response = client.get("/", params=params)
    assert response.status_code == status.HTTP_200_OK
    response_date = response.json()
    expectest_message = f"Hello {name}"
    assert "message" in response_date
    assert response_date["message"] == expectest_message, response_date
