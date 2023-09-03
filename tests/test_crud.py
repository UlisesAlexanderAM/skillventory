"""Tests for CRUD operations on skills.

This module contains tests for CRUD (create, read, update, delete) 
operations on skills using a test database session fixture.

Fixtures:
- get_db_session: Module scoped session fixture.
- setup_db: Function scoped setup/teardown fixture.  
- random_number: Function scoped random number fixture.
- skill_factory: Session scoped skill factory fixture.
- skill_1: Session scoped fixture for a sample skill.
- skill_2: Session scoped fixture for another sample skill.

The tests will execute CRUD operations on skills using the fixtures 
to test the CRUD functions and validate the results.
"""

import random
import sqlite3
from collections.abc import Callable, Sequence
from typing import Any, Iterator

import pytest
from sqlalchemy.orm import Session

from app.data import crud
from app.database import config
from app.models import schemas
from app.models.models import Skill as skill_model
from app.models.schemas import LevelOfConfidence
from app.models.schemas import SkillBase as skill_schema


@pytest.fixture(scope="module")
def get_db_session() -> Iterator[Session]:
    """Gets a database session fixture.

    Yields:
        db: The database session.

    This is a module scoped fixture that yields a database session.
    The session is closed after the test finishes executing.
    """
    db: Session = config.TestLocalSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_db(get_db_session: Session) -> Any:
    """Sets up and tears down the database for tests.

    Args:
        get_db_session: The database session fixture.

    This fixture will create all tables before each test runs
    and drop all tables after each test finishes using the
    provided database session. It is function scoped and
    auto-used to setup/teardown the database for all tests.
    """
    try:
        config.Base.metadata.create_all(bind=get_db_session.get_bind())
    finally:
        config.Base.metadata.drop_all(bind=get_db_session.get_bind())


@pytest.fixture(scope="function")
def random_number() -> Iterator[int]:
    """Gets a random number fixture.

    Yields:
        The random number.

    This is a function scoped fixture that yields a random number.
    The random number is reset after the test finishes executing.
    """
    yield int(random.random() * 100)


@pytest.fixture(scope="session")
def skill_factory() -> Iterator[Callable[[str, LevelOfConfidence], skill_schema]]:
    """Gets a skill factory fixture.

    Yields:
        The skill factory.

    This is a session scoped fixture that yields a skill factory.
    The skill factory is reset after the test finishes executing.
    """

    def _skill_factory(
        skill_name: str, level_of_confidence: LevelOfConfidence
    ) -> skill_schema:
        """Creates a Skill schema object.

        Args:
            skill_name  The name of the skill.
            level_of_confidence: The level of confidence for the skill.

        Returns:
            The created Skill schema object.

        This function takes in a skill name and level of confidence and returns a
        Skill schema object with those values. It is used as a factory function to
        create Skill objects for testing.
        """
        skill = schemas.SkillBase(
            skill_name=skill_name, level_of_confidence=level_of_confidence
        )
        return skill

    yield _skill_factory


@pytest.fixture(scope="session")
def skill_1(
    skill_factory: Callable[[str, LevelOfConfidence], skill_schema]
) -> Iterator[skill_schema]:
    """Gets a skill_1 fixture.

    Args:
        skill_factory: The skill factory fixture.

    Yields:
        skill_1: The skill_1 object.

    This is a session scoped fixture that uses the skill factory to create
    a skill_1 object with name 'python' and confidence level 'LEVEL_2'. It yields
    the created skill_1 object.
    """
    yield skill_factory("python", schemas.LevelOfConfidence.LEVEL_2)


@pytest.fixture(scope="session")
def skill_2(
    skill_factory: Callable[[str, LevelOfConfidence], skill_schema]
) -> Iterator[skill_schema]:
    """Gets a skill_2 fixture.

    Args:
        skill_factory: The skill factory fixture.

    Yields:
        skill_2: The skill_2 object.

    This is a session scoped fixture that uses the skill factory to create
    a skill_2 object with name 'typescript' and confidence level 'LEVEL_1'. It yields
    the created skill_2 object.
    """
    yield skill_factory("typescript", schemas.LevelOfConfidence.LEVEL_1)


@pytest.fixture(scope="function")
def create_one_skill(
    get_db_session: Session, skill_1: skill_schema
) -> Iterator[skill_schema]:
    """Creates one skill in the database.

    Args:
        get_db_session (Session): The database session fixture.
        skill_1 (skill_schema): The skill_1 fixture.

    Yields:
        _skill_1 (skill_schema): The created skill.

    This fixture uses the skill_1 fixture and database session
    to create one skill in the database. It yields the created
    skill object.
    """
    _skill_1: skill_schema = skill_1
    crud.create_skill(session=get_db_session, skill=_skill_1)
    yield _skill_1


@pytest.fixture(scope="function")
def create_two_skill(
    get_db_session: Session, create_one_skill: skill_schema, skill_2: skill_schema
) -> Iterator[tuple[skill_schema, skill_schema]]:
    """Creates two skills in the database.

    Args:
        get_db_session (Session): The database session fixture.
        create_one_skill (skill_schema): The skill_1 fixture.
        skill_2 (skill_schema): The skill_2 fixture.

    Yields:
        _skill_1 (skill_schema): The created skill_1 object.
        _skill_2 (skill_schema): The created skill_2 object.

    This fixture uses the skill_1 and skill_2 fixtures and database session
    to create two skills in the database. It yields the created
    skill_1 and skill_2 objects.
    """
    _skill_1: skill_schema = create_one_skill
    _skill_2: skill_schema = skill_2
    crud.create_skill(session=get_db_session, skill=_skill_2)
    yield _skill_1, _skill_2


@pytest.fixture(scope="function")
def get_skill_id(
    get_db_session: Session, create_one_skill: skill_schema
) -> Iterator[int]:
    """Gets the skill ID from the created skill.

    Args:
        get_db_session (Session): The database session fixture.
        create_one_skill (skill_schema): The created skill fixture.

    Yields:
        The ID of the created skill.

    This fixture gets the skill ID of the skill created by the
    create_one_skill fixture. It queries the database using the
    session and skill name.
    """
    _skill: skill_model | None = crud.get_skill_by_name(
        session=get_db_session, skill_name=create_one_skill.skill_name
    )
    if _skill is not None:
        yield _skill.skill_id


@pytest.fixture(scope="function")
def get_skill(
    get_db_session: Session, create_one_skill: skill_schema
) -> Iterator[skill_model]:
    """Gets the created skill from the database.

    Args:
        get_db_session (Session): The database session fixture.
        create_one_skill (skill_schema): The created skill fixture.

    Yields:
        _skill (skill_model): The created skill object.

    This fixture queries the database using the session and skill name
    from the create_one_skill fixture. It yields the skill object if found.
    """
    _skill: skill_model | None = crud.get_skill_by_name(
        session=get_db_session, skill_name=create_one_skill.skill_name
    )
    if _skill is not None:
        yield _skill


class TestGetSkillById:
    @staticmethod
    def test_get_skill_by_id(get_db_session: Session, get_skill_id: int) -> None:
        skill_by_id: skill_model | None = crud.get_skill_by_id(
            session=get_db_session, skill_id=get_skill_id
        )
        assert skill_by_id is not None
        assert skill_by_id.skill_id == 1

    @staticmethod
    def test_get_skill_by_id_none(get_db_session: Session, random_number: int) -> None:
        with pytest.warns(
            UserWarning, match=f"The skill with id {random_number} doesn't exists"
        ):
            crud.get_skill_by_id(session=get_db_session, skill_id=random_number)


class TestGetSkillByName:
    @staticmethod
    def test_get_skill_by_name(
        get_db_session: Session, create_one_skill: skill_schema
    ) -> None:
        skill: skill_model | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=create_one_skill.skill_name
        )
        assert skill is not None
        assert skill.skill_name == create_one_skill.skill_name
        assert skill.level_of_confidence == create_one_skill.level_of_confidence

    @staticmethod
    def test_get_skill_by_name_none(
        get_db_session: Session, skill_1: skill_schema
    ) -> None:
        with pytest.warns(
            UserWarning, match=f"The skill named {skill_1.skill_name} doesn't exists"
        ):
            crud.get_skill_by_name(
                session=get_db_session, skill_name=skill_1.skill_name
            )


class TestCreateSkill:
    @staticmethod
    def test_create_skill(
        get_db_session: Session, create_one_skill: skill_schema
    ) -> None:
        skill: skill_model | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=create_one_skill.skill_name
        )
        assert skill is not None
        assert skill.skill_name == create_one_skill.skill_name
        assert skill.level_of_confidence == create_one_skill.level_of_confidence

    @staticmethod
    def test_create_skill_already_exist(
        get_db_session: Session, skill_1: skill_schema
    ) -> None:
        with pytest.raises(sqlite3.IntegrityError) as exc_info:
            crud.create_skill(session=get_db_session, skill=skill_1)
            crud.create_skill(session=get_db_session, skill=skill_1)
        assert "The skill already exist" in str(exc_info.value)


class TestGetSkills:
    @staticmethod
    def test_get_zero_skills(get_db_session: Session) -> None:
        skill: Sequence[skill_model] = crud.get_skills(session=get_db_session)
        assert skill == []
        assert len(skill) == 0

    @staticmethod
    def test_get_one_skill(
        get_db_session: Session, create_one_skill: skill_schema
    ) -> None:
        skills: Sequence[skill_model] = crud.get_skills(get_db_session)
        assert len(skills) == 1
        assert skills[0].skill_name == create_one_skill.skill_name
        assert skills[0].level_of_confidence == create_one_skill.level_of_confidence

    @staticmethod
    def test_get_multiple_skills(
        get_db_session: Session, create_two_skill: tuple[skill_schema, skill_schema]
    ) -> None:
        skills: Sequence[skill_model] = crud.get_skills(get_db_session)
        skill_1, skill_2 = create_two_skill
        assert len(skills) == 2
        assert skills[0].skill_name == skill_1.skill_name
        assert skills[0].level_of_confidence == skill_1.level_of_confidence
        assert skills[1].skill_name == skill_2.skill_name
        assert skills[1].level_of_confidence == skill_2.level_of_confidence


class TestDeleteSkill:
    @staticmethod
    def test_delete_skill(get_db_session: Session, get_skill: skill_model) -> None:
        skill: skill_model | None = get_skill
        assert skill is not None
        crud.delete_skill(session=get_db_session, skill=skill)
        with pytest.warns(
            UserWarning, match=f"The skill named {skill.skill_name} doesn't exists"
        ):
            crud.get_skill_by_name(session=get_db_session, skill_name=skill.skill_name)

    @staticmethod
    def test_delete_skill_non_existent(
        get_db_session: Session, get_skill: skill_model
    ) -> None:
        skill: skill_model = get_skill
        crud.delete_skill(session=get_db_session, skill=skill)
        with pytest.warns(
            UserWarning, match=f"The skill named {skill.skill_name} doesn't exists"
        ):
            crud.get_skill_by_name(session=get_db_session, skill_name=skill.skill_name)


class TestUpdateSKill:
    @staticmethod
    def test_update_skill_name(
        get_db_session: Session, get_skill_id: int, skill_2: skill_schema
    ) -> None:
        skill_id: int = get_skill_id
        crud.update_skill_name(
            session=get_db_session, skill_id=skill_id, new_name=skill_2.skill_name
        )
        skill_updated: skill_model | None = crud.get_skill_by_id(
            session=get_db_session, skill_id=skill_id
        )
        assert skill_updated is not None
        assert skill_updated.skill_name == skill_2.skill_name
        assert skill_updated.skill_id == skill_id

    @staticmethod
    def test_update_skill_level_of_confidence(
        get_db_session: Session, get_skill_id: int, skill_2: skill_schema
    ) -> None:
        skill_id: int = get_skill_id
        crud.update_skill_level_of_confidence(
            session=get_db_session,
            skill_id=skill_id,
            new_level=skill_2.level_of_confidence,
        )
        skill_updated: skill_model | None = crud.get_skill_by_id(
            session=get_db_session, skill_id=skill_id
        )
        assert skill_updated is not None
        assert skill_updated.level_of_confidence == skill_2.level_of_confidence
        assert skill_updated.skill_id == skill_id
