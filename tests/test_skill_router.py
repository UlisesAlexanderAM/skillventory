from collections.abc import Sequence
from typing import Callable

import pytest
from fastapi import status, testclient
from httpx import Response

from skillventory import main
from skillventory.models import models

client = testclient.TestClient(app=main.app)

BASE_ROUTE = "/v1/skills"


@pytest.fixture()
def one_json_skill(
    factory_skills_json: Callable[[int], Sequence[dict[str, str]]],
) -> dict[str, str]:
    return factory_skills_json(1)[0]


@pytest.fixture()
def _post_one_skill(one_json_skill: dict[str, str]) -> None:
    skill = one_json_skill
    client.post(f"{BASE_ROUTE}/", json=skill)


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
        response = client.post(f"{BASE_ROUTE}/", json=factory_skills_json(1)[0])

    assert response.status_code == expected_status_code
    assert response.json() == expected_json


class TestGetSkills:
    default_limit = 15

    @pytest.fixture()
    def post_skills(
        self, factory_skills_json: Callable[[int], list[dict[str, str]]]
    ) -> Callable[[int], None]:
        def _post_skills(number_of_skills: int) -> None:
            skills_json = factory_skills_json(number_of_skills)
            for _ in range(number_of_skills):
                client.post(f"{BASE_ROUTE}/", json=skills_json[_])

        return _post_skills

    @pytest.mark.parametrize("num_skills", [0, 1, 2])
    def test_status_code(
        self,
        post_skills: Callable[[int], None],
        num_skills: int,
    ) -> None:
        post_skills(num_skills)
        response: Response = client.get(f"{BASE_ROUTE}/")

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        ("number_of_skills_created", "number_of_skills_received"), [(1, 1), (16, 15)]
    )
    def test_page_1(
        self,
        post_skills: Callable[[int], None],
        number_of_skills_created: int,
        number_of_skills_received: int,
    ):
        post_skills(number_of_skills_created)
        response = client.get(f"{BASE_ROUTE}/")

        assert len(response.json()) == number_of_skills_received

    @pytest.mark.parametrize(
        ("number_of_skills_created", "number_of_skills_received", "offset"),
        [(1, 1, 0), (16, 1, 15)],
    )
    def test_offset(
        self,
        post_skills: Callable[[int], None],
        number_of_skills_created: int,
        number_of_skills_received: int,
        offset: int,
    ):
        post_skills(number_of_skills_created)
        response = client.get(f"{BASE_ROUTE}/?offset={offset}")

        assert len(response.json()) == number_of_skills_received
        assert response.headers["X-Total-Count"] == str(number_of_skills_created)
        assert response.headers["X-Offset"] == str(offset)
        assert response.headers["X-Limit"] == str(self.default_limit)


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
        response: Response = client.get(f"{BASE_ROUTE}/id/{skill_id}")

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
        response: Response = client.get(f"{BASE_ROUTE}/name/{skill_name}")

        assert response.status_code == expected_status_code

    def test_content(self) -> None:
        skill_name = "python_0"
        response = client.get(f"{BASE_ROUTE}/name/{skill_name}")

        assert response.json() == {
            "skill_id": 1,
            "skill_name": skill_name,
            "level_of_confidence": models.LevelOfConfidence.LEVEL_1.value,
        }


@pytest.mark.usefixtures("_post_one_skill")
class TestUpdateSkillName:
    @pytest.fixture()
    def skill_name_modified(self, one_json_skill: dict[str, str]) -> dict[str, str]:
        skill_modified = one_json_skill.copy()
        skill_modified["skill_name"] = "Clojure"
        return skill_modified

    @pytest.mark.parametrize(
        ("skill_id", "expected_status_code"),
        [(1, status.HTTP_200_OK), (2, status.HTTP_404_NOT_FOUND)],
    )
    def test_update_name_status_code(
        self,
        skill_id: int,
        expected_status_code: int,
        skill_name_modified: dict[str, str],
    ) -> None:
        response = client.patch(f"{BASE_ROUTE}/{skill_id}", json=skill_name_modified)

        assert response.status_code == expected_status_code

    def test_update_name_content(self, skill_name_modified: dict[str, str]) -> None:
        skill_id = 1
        response = client.patch(f"{BASE_ROUTE}/{skill_id}", json=skill_name_modified)
        skill_received = skill_name_modified.copy()
        skill_received.update({"skill_id": skill_id})
        assert response.json() == skill_received


@pytest.mark.usefixtures("_post_one_skill")
class TestUpdateSkillLevel:
    @pytest.fixture()
    def skill_level_modified(self, one_json_skill: dict[str, str]) -> dict[str, str]:
        skill_modified = one_json_skill.copy()
        skill_modified["level_of_confidence"] = models.LevelOfConfidence.LEVEL_2.value
        return skill_modified

    @pytest.mark.parametrize(
        ("skill_id", "expected_status_code"),
        [(1, status.HTTP_200_OK), (2, status.HTTP_404_NOT_FOUND)],
    )
    def test_update_level_status_code(
        self,
        skill_id: int,
        expected_status_code: int,
        skill_level_modified: dict[str, str],
    ) -> None:
        response = client.patch(f"{BASE_ROUTE}/{skill_id}", json=skill_level_modified)

        assert response.status_code == expected_status_code

    def test_update_level_content(self, skill_level_modified: dict[str, str]) -> None:
        skill_id = 1
        response = client.patch(f"{BASE_ROUTE}/{skill_id}", json=skill_level_modified)
        skill_received = skill_level_modified.copy()
        skill_received.update({"skill_id": skill_id})
        assert response.json() == skill_received
