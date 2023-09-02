import pytest
import sqlite3
import random
from sqlalchemy import orm
from typing import Any

from app.database import config
from app.data import crud
from app.models import schemas, models


@pytest.fixture(scope="module")
def get_db_session():
    db = config.TestLocalSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def setup_db(get_db_session: orm.Session):
    try:
        yield config.Base.metadata.create_all(bind=get_db_session.get_bind())
    finally:
        config.Base.metadata.drop_all(bind=get_db_session.get_bind())


SKILL_1 = schemas.SkillBase(
    skill_name="python", level_of_confidence=schemas.LevelOfConfidence.LEVEL_2
)
SKILL_2 = schemas.SkillBase(
    skill_name="typescript",
    level_of_confidence=schemas.LevelOfConfidence.LEVEL_1,
)


class TestGetSkillById:
    @staticmethod
    def test_get_skill_by_id(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(session=get_db_session, skill=SKILL_1)
        skill_by_name: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        assert skill_by_name is not None
        skill_id = skill_by_name.skill_id
        skill_by_id = crud.get_skill_by_id(session=get_db_session, skill_id=skill_id)
        assert skill_by_id is not None
        assert skill_by_id == skill_by_name

    @staticmethod
    def test_get_skill_by_id_none(get_db_session: orm.Session, setup_db: Any) -> None:
        random_number = int(random.random() * 100)
        skill = crud.get_skill_by_id(session=get_db_session, skill_id=random_number)
        assert skill is None


class TestGetSkillByName:
    @staticmethod
    def test_get_skill_by_name(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(get_db_session, SKILL_1)
        skill: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        assert skill is not None
        assert skill.skill_name == SKILL_1.skill_name
        assert skill.level_of_confidence == SKILL_1.level_of_confidence

    @staticmethod
    def test_get_skill_by_name_none(get_db_session: orm.Session, setup_db: Any) -> None:
        skill: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        assert skill is None


class TestCreateSkill:
    @staticmethod
    def test_create_skill(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(session=get_db_session, skill=SKILL_1)
        skill: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        assert skill is not None
        assert skill.skill_name == SKILL_1.skill_name
        assert skill.level_of_confidence == SKILL_1.level_of_confidence

    @staticmethod
    def test_create_skill_already_exist(get_db_session: orm.Session, setup_db: Any):
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            crud.create_skill(session=get_db_session, skill=SKILL_1)
            crud.create_skill(session=get_db_session, skill=SKILL_1)
        assert "The skill already exist" in str(exc_info.value)


class TestGetSkills:
    @staticmethod
    def test_get_zero_skills(get_db_session: orm.Session, setup_db: Any) -> None:
        skill = crud.get_skills(get_db_session)
        assert skill == []
        assert len(skill) == 0

    @staticmethod
    def test_get_one_skill(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(session=get_db_session, skill=SKILL_1)
        skills = crud.get_skills(get_db_session)
        assert len(skills) == 1
        assert skills[0].skill_name == SKILL_1.skill_name
        assert skills[0].level_of_confidence == SKILL_1.level_of_confidence

    @staticmethod
    def test_get_multiple_skills(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(get_db_session, SKILL_1)
        crud.create_skill(get_db_session, SKILL_2)
        skills = crud.get_skills(get_db_session)
        assert len(skills) == 2
        assert skills[0].skill_name == SKILL_1.skill_name
        assert skills[0].level_of_confidence == SKILL_1.level_of_confidence
        assert skills[1].skill_name == SKILL_2.skill_name
        assert skills[1].level_of_confidence == SKILL_2.level_of_confidence


class TestDeleteSkill:
    @staticmethod
    def test_delete_skill(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(session=get_db_session, skill=SKILL_1)
        skill: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        crud.delete_skill(session=get_db_session, skill=skill)
        skill = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        assert skill is None

    @staticmethod
    def test_delete_skill_non_existent(
        get_db_session: orm.Session, setup_db: Any
    ) -> None:
        skill: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        crud.delete_skill(session=get_db_session, skill=skill)
        skill = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
        assert skill is None
