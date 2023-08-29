import pytest
import sqlalchemy
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


class TestCreateSkill:
    @staticmethod
    def test_create_skill(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(get_db_session, SKILL_1)
        stmt: sqlalchemy.Select[tuple[models.Skill]] = sqlalchemy.select(
            models.Skill
        ).where(models.Skill.skill_name == "python")
        skill_db = get_db_session.scalars(stmt).one_or_none()
        assert skill_db.skill_name == "python"
        assert skill_db.level_of_confidence == schemas.LevelOfConfidence.LEVEL_2


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
        assert skills[0].skill_name == "python"
        assert skills[0].level_of_confidence == schemas.LevelOfConfidence.LEVEL_2

    @staticmethod
    def test_get_multiple_skills(get_db_session: orm.Session, setup_db: Any) -> None:
        crud.create_skill(get_db_session, SKILL_1)
        crud.create_skill(get_db_session, SKILL_2)
        skills = crud.get_skills(get_db_session)
        assert len(skills) == 2
        assert skills[0].skill_name == "python"
        assert skills[0].level_of_confidence == schemas.LevelOfConfidence.LEVEL_2
        assert skills[1].skill_name == "typescript"
        assert skills[1].level_of_confidence == schemas.LevelOfConfidence.LEVEL_1
