import pytest
import sqlalchemy
from sqlalchemy import orm

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


def test_create_skill(get_db_session, setup_db):
    skill = schemas.SkillBase(
        skill_name="python", level_of_confidence=schemas.LevelOfConfidence.LEVEL_1
    )
    crud.create_skill(get_db_session, skill)
    stmt: sqlalchemy.Select[tuple[models.Skill]] = sqlalchemy.select(
        models.Skill
    ).where(models.Skill.skill_name == "python")
    skill_db = get_db_session.scalars(stmt).one_or_none()
    assert skill_db.skill_name == "python"
    assert skill_db.level_of_confidence == schemas.LevelOfConfidence.LEVEL_1


class TestGetSkills:
    skill_1 = schemas.SkillBase(
        skill_name="python", level_of_confidence=schemas.LevelOfConfidence.LEVEL_2
    )
    skill_2 = schemas.SkillBase(
        skill_name="typescript",
        level_of_confidence=schemas.LevelOfConfidence.LEVEL_1,
    )

    def test_get_zero_skills(self, get_db_session, setup_db):
        skill = crud.get_skills(get_db_session)
        assert skill == []
        assert len(skill) == 0

    def test_get_one_skill(self, get_db_session, setup_db):
        crud.create_skill(session=get_db_session, skill=self.skill_1)
        skills = crud.get_skills(get_db_session)
        assert len(skills) == 1
        assert skills[0].skill_name == "python"
        assert skills[0].level_of_confidence == schemas.LevelOfConfidence.LEVEL_2

    def test_get_multiple_skills(self, get_db_session, setup_db):
        crud.create_skill(get_db_session, self.skill_1)
        crud.create_skill(get_db_session, self.skill_2)
        skills = crud.get_skills(get_db_session)
        assert len(skills) == 2
        assert skills[0].skill_name == "python"
        assert skills[0].level_of_confidence == schemas.LevelOfConfidence.LEVEL_2
        assert skills[1].skill_name == "typescript"
        assert skills[1].level_of_confidence == schemas.LevelOfConfidence.LEVEL_1
