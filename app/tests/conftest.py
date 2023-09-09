from collections.abc import Callable, Iterator
from typing import Any

import pytest
from sqlalchemy.orm import Session

from app.data import crud
from app.database import config
from app.models import schemas
from app.models.models import Skill as skill_model
from app.models.schemas import LevelOfConfidence, skill_base_schema


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
        yield config.Base.metadata.create_all(bind=get_db_session.get_bind())
    finally:
        config.Base.metadata.drop_all(bind=get_db_session.get_bind())


@pytest.fixture(scope="session")
def skill_factory() -> Iterator[Callable[[str, LevelOfConfidence], skill_base_schema]]:
    """Gets a skill factory fixture.

    Yields:
        The skill factory.

    This is a session scoped fixture that yields a skill factory.
    The skill factory is reset after the test finishes executing.
    """

    def _skill_factory(
        skill_name: str, level_of_confidence: LevelOfConfidence
    ) -> skill_base_schema:
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
    skill_factory: Callable[[str, LevelOfConfidence], skill_base_schema]
) -> Iterator[skill_base_schema]:
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
    skill_factory: Callable[[str, LevelOfConfidence], skill_base_schema]
) -> Iterator[skill_base_schema]:
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
    get_db_session: Session, skill_1: skill_base_schema
) -> Iterator[skill_base_schema]:
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
    _skill_1: skill_base_schema = skill_1
    crud.create_skill(session=get_db_session, skill=_skill_1)
    yield _skill_1


@pytest.fixture(scope="function")
def create_two_skill(
    get_db_session: Session,
    create_one_skill: skill_base_schema,
    skill_2: skill_base_schema,
) -> Iterator[tuple[skill_base_schema, skill_base_schema]]:
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
    _skill_1: skill_base_schema = create_one_skill
    _skill_2: skill_base_schema = skill_2
    crud.create_skill(session=get_db_session, skill=_skill_2)
    yield _skill_1, _skill_2


@pytest.fixture(scope="function")
def get_skill_id(
    get_db_session: Session, create_one_skill: skill_base_schema
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
