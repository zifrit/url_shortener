import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    response_date = response.json()
    expectest_message = "Hello World"
    assert "message" in response_date
    assert response_date["message"] == expectest_message, response_date


@pytest.mark.parametrize(
    "name",
    [
        "name",
        "Mike",
        "",
        "%#@",
    ],
)
def test_root_view_with_custom_name(
    name: str,
    client: TestClient,
) -> None:
    params = {"name": name}
    response = client.get("/", params=params)
    assert response.status_code == status.HTTP_200_OK
    response_date = response.json()
    expectest_message = f"Hello {name}"
    assert "message" in response_date
    assert response_date["message"] == expectest_message, response_date
