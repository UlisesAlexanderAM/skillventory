"""Fixtures for pytest tests.

This module contains shared fixtures used in the pytest test suite.

Fixtures:

- get_db_session: Module scoped session fixture.
- setup_db: Function scoped setup/teardown fixture.
- skill_factory: Session scoped skill factory fixture.
- skill_1: Sample skill fixture.
- skill_2: Another sample skill fixture.
- create_one_skill: Creates one skill fixture.
- create_two_skills: Creates two skills fixture.
- get_skill_id: Gets ID of created skill fixture.

The fixtures handle setup/teardown of the database for each test function
and provide reusable objects for tests.
"""

from collections.abc import Callable, Iterator, Sequence
from typing import Any

import pytest
from _pytest import logging
from loguru import logger
from sqlalchemy.orm import Session

from app import main
from app.data import crud, dependencies
from app.database import config
from app.models import schemas
from app.models.type_aliases import level_of_confidence, skill_base_schema


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


@pytest.fixture(scope="function")
def override_get_db_session() -> Any:
    """Override get_db_session dependecy.

    This is a module scoped fixture that overrides the get_db_session
    dependency for a function tailored for testing purposes.
    The sesion is closed after the test finishes executing.
    """

    def get_db_session() -> Iterator[Session]:
        db: Session = config.TestLocalSession()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[dependencies.get_db_session] = get_db_session


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
def skill_factory() -> (
    Iterator[Callable[[str, level_of_confidence], skill_base_schema]]
):
    """Gets a skill factory fixture.

    Yields:
        The skill factory.

    This is a session scoped fixture that yields a skill factory.
    The skill factory is reset after the test finishes executing.
    """

    def _skill_factory(
        skill_name: str, level_of_confidence: level_of_confidence
    ) -> skill_base_schema:
        """Creates a Skill schema object.

        Args:
            skill_name: The name of the skill.
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
    skill_factory: Callable[[str, level_of_confidence], skill_base_schema]
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
    skill_factory: Callable[[str, level_of_confidence], skill_base_schema]
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


@pytest.fixture(scope="session")
def skills_json(
    skill_1: skill_base_schema, skill_2: skill_base_schema
) -> Iterator[Sequence[dict[str, str]]]:
    """Gets a list of skills in dict/json form.

    Args:
        skill_1: The skill_1 fixture
        skill_2: The skill_2 fixture

    Yields:
        A sequence of skills.

    This is a session scope fixture that uses the skill_1 and skill_2 fixtures
    to create a sequence of skills dicts/json. It yields the created sequence.
    """
    yield [
        {
            "skill_name": skill_1.skill_name,
            "level_of_confidence": skill_1.level_of_confidence.value,
        },
        {
            "skill_name": skill_2.skill_name,
            "level_of_confidence": skill_2.level_of_confidence.value,
        },
    ]


@pytest.fixture(scope="function")
def create_one_skill(
    get_db_session: Session, skill_1: skill_base_schema
) -> Iterator[skill_base_schema]:
    """Creates one skill in the database.

    Args:
        get_db_session: The database session fixture.
        skill_1: The skill_1 fixture.

    Yields:
        _skill_1: The created skill.

    This fixture uses the skill_1 fixture and database session
    to create one skill in the database. It yields the created
    skill object.
    """
    _skill_1: skill_base_schema = skill_1
    crud.create_skill(session=get_db_session, skill=_skill_1)
    yield _skill_1


@pytest.fixture
def reportlog(pytestconfig):  # noqa: D103 # type: ignore
    logging_plugin = pytestconfig.pluginmanager.getplugin("logging-plugin")  # type: ignore
    handler_id = logger.add(logging_plugin.report_handler, format="{message}")  # type: ignore
    yield
    logger.remove(handler_id)


@pytest.fixture
def caplog(caplog: logging.LogCaptureFixture):  # noqa: D103
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)
