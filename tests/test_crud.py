import pytest
import sqlalchemy
from sqlalchemy import orm
import sqlite3
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


class TestGetSkillByName:
    @staticmethod
    def test_get_skill_by_name(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(get_db_session, SKILL_1)
        skill: models.Skill | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=SKILL_1.skill_name
        )
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
