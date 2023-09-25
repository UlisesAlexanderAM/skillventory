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


@pytest.mark.parametrize(
    "expected_status_code,expected_json, num_skills",
    [
        (status.HTTP_201_CREATED, {"message": "Skill added successfully"}, 1),
        (status.HTTP_409_CONFLICT, {"detail": "Skill already added"}, 2),
    ],
)
def test_post_skill(expected_status_code, expected_json, num_skills, skill_1) -> None:
    for _ in range(num_skills):
        response = client.post(
            "/skills",
            json={
                "skill_name": skill_1.skill_name,
                "level_of_confidence": skill_1.level_of_confidence.value,
            },
        )

    assert response.status_code == expected_status_code
    assert response.json() == expected_json
