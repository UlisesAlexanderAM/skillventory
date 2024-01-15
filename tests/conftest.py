from collections.abc import Callable, Iterator
from typing import Any

import pytest
from _pytest import logging
from loguru import logger
import sqlmodel

from app import main
from app.data import crud, dependencies
from app.database import config
from app.models import models


@pytest.fixture(scope="function")
def get_db_session() -> Iterator[sqlmodel.Session]:
    """Gets a database session fixture.

    Yields:
        db: The database session.

    This is a module scoped fixture that yields a database session.
    The session is closed after the test finishes executing.
    """
    with sqlmodel.Session(config.testing_engine) as session:
        yield session


@pytest.fixture(scope="function")
def override_get_db_session() -> Any:
    """Override get_db_session dependecy.

    This is a module scoped fixture that overrides the get_db_session
    dependency for a function tailored for testing purposes.
    The sesion is closed after the test finishes executing.
    """

    def get_db_session() -> Iterator[sqlmodel.Session]:
        with sqlmodel.Session(config.testing_engine) as session:
            yield session

    main.app.dependency_overrides[dependencies.get_db_session] = get_db_session
    try:
        yield config.Base.metadata.create_all(bind=config.testing_engine)
    finally:
        config.Base.metadata.drop_all(bind=config.testing_engine)


@pytest.fixture(scope="function", autouse=True)
def setup_db(get_db_session: sqlmodel.Session) -> Any:
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
def factory_skills_models() -> Iterator[Callable[[int], list[models.SkillBase]]]:
    """Factory to create a list of SkillBase models."""

    def _skills_models(number_of_skills: int) -> list[models.SkillBase]:
        skills_names: list[str] = [f"python_{x}" for x in range(number_of_skills)]
        level_of_confidence: list[models.LevelOfConfidence] = [
            models.LevelOfConfidence.LEVEL_1 for _ in range(number_of_skills)
        ]
        skills: list[models.SkillBase] = []
        for _ in range(number_of_skills):
            skills.append(
                models.SkillBase(
                    skill_name=skills_names[_],
                    level_of_confidence=level_of_confidence[_],
                )
            )
        return skills

    yield _skills_models


@pytest.fixture(scope="session")
def factory_skills_json() -> Iterator[Callable[[int], list[dict[str, str]]]]:
    """Factory to create a list of skills in json-like format."""

    def _skills_json(number_of_skills: int) -> list[dict[str, str]]:
        skills_names: list[str] = [f"python_{x}" for x in range(number_of_skills)]
        level_of_confidence: list[str] = [
            models.LevelOfConfidence.LEVEL_1.value for _ in range(number_of_skills)
        ]
        skills: list[dict[str, str]] = []
        for _ in range(number_of_skills):
            keys = ("skill_name", "level_of_confidence")
            value = (skills_names[_], level_of_confidence[_])
            skills.append(dict(zip(keys, value, strict=True)))
        return skills

    yield _skills_json


@pytest.fixture(scope="function")
def factory_skills_in_db(
    get_db_session: sqlmodel.Session,
    factory_skills_models: Callable[[int], list[models.SkillBase]],
) -> Iterator[Callable[[int], list[models.SkillBase]]]:
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

    def _skills_in_db(number_of_skills: int) -> list[models.SkillBase]:
        skills: list[models.SkillBase] = factory_skills_models(number_of_skills)
        for _ in range(number_of_skills):
            crud.create_skill(session=get_db_session, skill=skills[_])
        return skills

    yield _skills_in_db


@pytest.fixture
def reportlog(pytestconfig: Any):
    logging_plugin = pytestconfig.pluginmanager.getplugin("logging-plugin")
    handler_id = logger.add(logging_plugin.report_handler, format="{message}")
    yield
    logger.remove(handler_id)


@pytest.fixture
def caplog(caplog: logging.LogCaptureFixture) -> Iterator[logging.LogCaptureFixture]:
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)
