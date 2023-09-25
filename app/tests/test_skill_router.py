import pytest
from fastapi import status, testclient
from httpx import Response

from app import main

client = testclient.TestClient(app=main.app)


@pytest.mark.usefixtures("override_get_db_session")
@pytest.mark.parametrize("num_skills", [0, 1, 2])
def test_get_skills(num_skills: int, skills_json) -> None:
    for _ in range(num_skills):
        client.post("/skills", json=skills_json[_])
    response: Response = client.get("/skills")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == num_skills