from collections.abc import Sequence
from typing import Callable

import pytest
from fastapi import status, testclient
from httpx import Response

from app import main

client = testclient.TestClient(app=main.app)


@pytest.fixture()
def one_json_skill(
    factory_skills_json: Callable[[int], Sequence[dict[str, str]]],
) -> dict[str, str]:
    return factory_skills_json(1)[0]


@pytest.fixture()
def _post_one_skill(one_json_skill: dict[str, str]) -> None:
    skill = one_json_skill
    client.post("/skills", json=skill)


@pytest.mark.usefixtures("override_get_db_session")
@pytest.mark.parametrize(
    ("expected_status_code", "expected_json", "num_skills"),
    [
        (status.HTTP_201_CREATED, {"message": "Skill added successfully"}, 1),
        (status.HTTP_409_CONFLICT, {"detail": "Skill already added"}, 2),
    ],
)
def test_post_skill(
    expected_status_code: int,
    expected_json: Sequence[dict[str, str]],
    num_skills: int,
    factory_skills_json: Callable[[int], list[dict[str, str]]],
) -> None:
    for _ in range(num_skills):
        response = client.post("/skills", json=factory_skills_json(1)[0])

    assert response.status_code == expected_status_code
    assert response.json() == expected_json


@pytest.mark.parametrize("num_skills", [0, 1, 2])
def test_get_skills(
    num_skills: int,
    factory_skills_json: Callable[[int], list[dict[str, str]]],
) -> None:
    skills_json = factory_skills_json(2)

    for _ in range(num_skills):
        client.post("/skills", json=skills_json[_])
    response: Response = client.get("/skills")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == num_skills
    assert response.headers["X-Total-Count"] == str(num_skills)


@pytest.mark.usefixtures("_post_one_skill")
class TestGetSkillById:
    @pytest.mark.parametrize(
        ("skill_id", "expected_status_code"),
        [(1, status.HTTP_200_OK), (2, status.HTTP_404_NOT_FOUND)],
    )
    def test_status_code(
        self,
        skill_id: int,
        expected_status_code: int,
    ) -> None:
        response: Response = client.get(f"/skills/id/{skill_id}")

        assert response.status_code == expected_status_code


@pytest.mark.usefixtures("_post_one_skill")
class TestGetSkillByName:
    @pytest.mark.parametrize(
        ("skill_name", "expected_status_code"),
        [("python_0", status.HTTP_200_OK), ("java", status.HTTP_404_NOT_FOUND)],
    )
    def test_status_code(
        self,
        skill_name: str,
        expected_status_code: int,
    ) -> None:
        response: Response = client.get(f"/skills/name/{skill_name}")

        assert response.status_code == expected_status_code
