from collections.abc import Sequence, Callable
from typing import Any, Literal, Optional

import pytest
import sqlmodel

from app.data import crud
from app.models import models

MULTIPLE_SKILLS = 2


@pytest.mark.parametrize("skill_id,expected_warning", [(1, False), (2, True)])
def test_get_skill_by_id(
    get_db_session: sqlmodel.Session,
    factory_skills_in_db: Callable[[int], list[models.SkillBase]],
    skill_id: int,
    expected_warning: bool,
    caplog: Any,
) -> None:
    factory_skills_in_db(1)
    skill: Optional[models.Skill] = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )

    if expected_warning:
        assert f"The skill with id {skill_id} doesn't exists" in caplog.text
    else:
        assert skill is not None
        assert skill.skill_id == skill_id
        assert "Operation 'get_skill_by_id' ended successfully" in caplog.text


@pytest.mark.parametrize(
    "skill_name,expected_warning", [("python_0", False), ("java", True)]
)
def test_get_skill_by_name(
    get_db_session: sqlmodel.Session,
    factory_skills_in_db: Callable[[int], list[models.SkillBase]],
    skill_name: str,
    expected_warning: bool,
    caplog: Any,
) -> None:
    skill_from_fixture = factory_skills_in_db(1)[0]
    skill = crud.get_skill_by_name(session=get_db_session, skill_name=skill_name)

    if expected_warning:
        assert f"The skill named {skill_name} doesn't exists" in caplog.text
    else:
        assert skill is not None
        assert skill.skill_name == skill_from_fixture.skill_name


@pytest.mark.parametrize("expected_exception", [False, True])
def test_create_skill(
    get_db_session: sqlmodel.Session,
    factory_skills_models: Callable[[int], list[models.SkillBase]],
    expected_exception: bool,
    caplog: Any,
) -> None:
    skill_model: models.SkillBase = factory_skills_models(1)[0]
    crud.create_skill(session=get_db_session, skill=skill_model)
    skill: Optional[models.Skill] = crud.get_skill_by_name(
        session=get_db_session, skill_name=skill_model.skill_name
    )
    assert skill is not None
    assert skill.skill_name == skill_model.skill_name
    assert skill.level_of_confidence == skill_model.level_of_confidence

    if expected_exception:
        crud.create_skill(session=get_db_session, skill=skill_model)
        assert f"Skill {skill.skill_name} already exist" in caplog.text


@pytest.mark.parametrize("skill_id", [1, 2])
def test_delete_skill(
    get_db_session: sqlmodel.Session,
    factory_skills_in_db: Callable[[int], list[models.SkillBase]],
    skill_id: int,
) -> None:
    factory_skills_in_db(1)
    skill: Optional[models.Skill] = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )
    crud.delete_skill(session=get_db_session, skill=skill)
    assert crud.get_skill_by_id(session=get_db_session, skill_id=skill_id) is None


@pytest.mark.parametrize("skill_id,expected_warning", [(1, False), (2, True)])
def test_update_skill_name(
    get_db_session: sqlmodel.Session,
    factory_skills_in_db: Callable[[int], list[models.SkillBase]],
    factory_skills_models: Callable[[int], list[models.SkillBase]],
    skill_id: Literal[1, 2],
    expected_warning: bool,
    caplog: Any,
) -> None:
    factory_skills_in_db(1)
    skill_2: models.SkillBase = factory_skills_models(2)[1]
    crud.update_skill_name(
        session=get_db_session, skill_id=skill_id, new_name=skill_2.skill_name
    )
    skill_updated: Optional[models.Skill] = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )
    if expected_warning:
        assert f"The skill with id {skill_id} doesn't exist" in caplog.text
    else:
        assert skill_updated is not None
        assert skill_updated.skill_id == skill_id
        assert skill_updated.skill_name == skill_2.skill_name


@pytest.mark.parametrize("skill_id,expected_warning", [(1, False), (2, True)])
def test_update_skill_level_of_confidence(
    get_db_session: sqlmodel.Session,
    factory_skills_in_db: Callable[[int], list[models.SkillBase]],
    factory_skills_models: Callable[[int], list[models.SkillBase]],
    skill_id: int,
    expected_warning: bool,
    caplog: Any,
) -> None:
    factory_skills_in_db(1)
    skill_2: models.SkillBase = factory_skills_models(2)[1]

    crud.update_skill_level_of_confidence(
        session=get_db_session,
        skill_id=skill_id,
        new_level=skill_2.level_of_confidence,
    )
    skill_updated: Optional[models.Skill] = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )

    if expected_warning:
        assert f"The skill with id {skill_id} doesn't exist" in caplog.text
    else:
        assert skill_updated is not None
        assert skill_updated.skill_id == skill_id
        assert skill_updated.level_of_confidence == skill_2.level_of_confidence


class TestGetSkills:
    @pytest.mark.parametrize("number_of_skills", [0, 1, 2])
    def test_get_skills(
        self,
        get_db_session: sqlmodel.Session,
        factory_skills_in_db: Callable[[int], list[models.SkillBase]],
        number_of_skills: int,
    ) -> None:
        skills_wanted: Sequence[models.SkillBase] = factory_skills_in_db(
            number_of_skills
        )
        skills_db: Sequence[models.Skill] = crud.get_skills(session=get_db_session)

        assert len(skills_db) == number_of_skills

        for skill_wanted, skill_db in zip(skills_wanted, skills_db, strict=True):
            assert skill_db.skill_name == skill_wanted.skill_name
            assert skill_db.level_of_confidence == skill_wanted.level_of_confidence

    @pytest.mark.parametrize(
        "number_of_skills_created, number_of_skills_received", [(1, 1), (16, 15)]
    )
    def test_get_skills_page_1(
        self,
        get_db_session: sqlmodel.Session,
        factory_skills_in_db: Callable[[int], list[models.SkillBase]],
        number_of_skills_created: int,
        number_of_skills_received: int,
    ) -> None:
        factory_skills_in_db(number_of_skills_created)

        skills_db: Sequence[models.Skill] = crud.get_skills(session=get_db_session)

        assert len(skills_db) == number_of_skills_received

    @pytest.mark.parametrize(
        "number_of_skills_created, number_of_skills_received, offset",
        [(1, 1, 0), (16, 1, 15)],
    )
    def test_get_skill_offset(
        self,
        get_db_session: sqlmodel.Session,
        factory_skills_in_db: Callable[[int], Sequence[models.SkillBase]],
        number_of_skills_created: int,
        number_of_skills_received: int,
        offset: int,
    ) -> None:
        factory_skills_in_db(number_of_skills_created)

        skills_db: Sequence[models.Skill] = crud.get_skills(
            session=get_db_session, offset=offset
        )

        assert len(skills_db) == number_of_skills_received
