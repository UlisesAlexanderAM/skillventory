"""Tests for CRUD operations on skills.

This module contains tests for CRUD (create, read, update, delete) 
operations on skills using a test database session fixture.

Fixtures:
- get_db_session: Module scoped session fixture.
- setup_db: Function scoped setup/teardown fixture.  
- skill_factory: Session scoped skill factory fixture.
- skill_1: Session scoped fixture for a sample skill.
- skill_2: Session scoped fixture for another sample skill.

The tests will execute CRUD operations on skills using the fixtures 
to test the CRUD functions and validate the results.
"""

import sqlite3
from collections.abc import Callable, Sequence, Iterator
from typing import Any, Literal

import pytest
from sqlalchemy.orm import Session

from app.data import crud
from app.database import config
from app.models import schemas
from app.models.models import Skill as skill_model
from app.models.schemas import LevelOfConfidence
from app.models.schemas import skill_base_schema


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


@pytest.mark.parametrize("skill_id,expected_warning", [(1, None), (2, UserWarning)])
def test_get_skill_by_id(
    get_db_session: Session,
    create_one_skill: skill_model,
    skill_id: int,
    expected_warning: Any,
) -> None:
    """Tests getting a skill by ID.

    Args:
        get_db_session: The database session fixture.
        create_one_skill: The create_one_skill fixture.
        skill_id: The ID of the skill to get.
        expected_warning: The expected warning or None.

    This test is parameterized on skill_id and expected_warning.
    It gets a skill by ID from the database using the crud.get_skill_by_id()
    function.

    It expects a UserWarning if the skill does not exist, or no warning if it does.
    The warning match is checked and the returned skill is validated if no warning.
    """
    with pytest.warns(
        expected_warning=expected_warning,
        match=f"The skill with id {skill_id} doesn't exists",
    ):
        skill: skill_model | None = crud.get_skill_by_id(
            session=get_db_session, skill_id=skill_id
        )

        if expected_warning is None:
            assert skill is not None
            assert skill.skill_id == skill_id


@pytest.mark.parametrize(
    "skill_name,expected_warning", [("python", None), ("java", UserWarning)]
)
def test_get_skill_by_name(
    get_db_session: Session,
    create_one_skill: skill_base_schema,
    skill_name: str,
    expected_warning: Any,
) -> None:
    """Tests get_skill_by_name

    Args:
        get_db_session: Database session fixture
        create_one_skill: Skill fixture
        skill_name: Skill name
        expected_warning: Expected warning

    This test gets the skill by name for an existing and non-existing skill.
    If the skill is found, no warning is expected. If not found, a warning is expected.
    If the skill is found, assert it matches the created skill.
    """
    with pytest.warns(
        expected_warning=expected_warning,
        match=f"The skill named {skill_name} doesn't exists",
    ):
        skill: skill_model | None = crud.get_skill_by_name(
            session=get_db_session, skill_name=skill_name
        )

        if expected_warning is None:
            assert skill is not None
            assert skill.skill_name == create_one_skill.skill_name


@pytest.mark.parametrize("expected_exception", [None, sqlite3.IntegrityError])
def test_create_skill(
    get_db_session: Session, skill_1: skill_base_schema, expected_exception: Any
) -> None:
    """Tests creating a skill.

    Args: get_db_session: The database session fixture.
    skill_1: The skill object fixture.
    expected_exception: The expected exception or None.

    This test does the following:
    - Creates a new skill using the skill_1 fixture.
    - Retrieves the created skill and validates it matches skill_1.
    - Tries creating the skill again which should raise an IntegrityError.
    - Validates the error message and exception type.
    """
    crud.create_skill(session=get_db_session, skill=skill_1)
    skill: skill_model | None = crud.get_skill_by_name(
        session=get_db_session, skill_name=skill_1.skill_name
    )
    assert skill is not None
    assert skill.skill_name == skill_1.skill_name
    assert skill.level_of_confidence == skill_1.level_of_confidence

    if expected_exception is not None:
        with pytest.raises(expected_exception=expected_exception) as exc_info:
            crud.create_skill(session=get_db_session, skill=skill_1)
        assert "The skill already exist" in str(exc_info.value)
        assert exc_info.type is sqlite3.IntegrityError


class TestGetSkills:
    @staticmethod
    def test_get_zero_skills(get_db_session: Session) -> None:
        skill: Sequence[skill_model] = crud.get_skills(session=get_db_session)
        assert skill == []
        assert len(skill) == 0

    @staticmethod
    def test_get_one_skill(
        get_db_session: Session, create_one_skill: skill_base_schema
    ) -> None:
        skills: Sequence[skill_model] = crud.get_skills(get_db_session)
        assert len(skills) == 1
        assert skills[0].skill_name == create_one_skill.skill_name
        assert skills[0].level_of_confidence == create_one_skill.level_of_confidence

    @staticmethod
    def test_get_multiple_skills(
        get_db_session: Session,
        create_two_skill: tuple[skill_base_schema, skill_base_schema],
    ) -> None:
        skills: Sequence[skill_model] = crud.get_skills(get_db_session)
        skill_1, skill_2 = create_two_skill
        assert len(skills) == 2
        assert skills[0].skill_name == skill_1.skill_name
        assert skills[0].level_of_confidence == skill_1.level_of_confidence
        assert skills[1].skill_name == skill_2.skill_name
        assert skills[1].level_of_confidence == skill_2.level_of_confidence


@pytest.mark.parametrize("number_of_skills", [0, 1, 2])
def test_get_skills(
    get_db_session: Session,
    skill_1: skill_base_schema,
    skill_2: skill_base_schema,
    number_of_skills: Literal[0, 1, 2],
) -> None:
    if number_of_skills == 1:
        crud.create_skill(session=get_db_session, skill=skill_1)
    elif number_of_skills == 2:
        crud.create_skill(session=get_db_session, skill=skill_1)
        crud.create_skill(session=get_db_session, skill=skill_2)
    skills: Sequence[skill_model] = crud.get_skills(session=get_db_session)
    assert len(skills) == number_of_skills
    if number_of_skills == 1:
        assert skills[0].skill_name == skill_1.skill_name
        assert skills[0].level_of_confidence == skill_1.level_of_confidence
        assert skills[0].skill_id == 1
    elif number_of_skills == 2:
        assert skills[0].skill_name == skill_1.skill_name
        assert skills[0].level_of_confidence == skill_1.level_of_confidence
        assert skills[0].skill_id == 1
        assert skills[1].skill_name == skill_2.skill_name
        assert skills[1].level_of_confidence == skill_2.level_of_confidence
        assert skills[1].skill_id == 2


@pytest.mark.parametrize("skill_id", [1, 2])
def test_delete_skill(
    get_db_session: Session, create_one_skill: skill_model, skill_id: Literal[1, 2]
):
    with pytest.warns(
        expected_warning=UserWarning,
        match=f"The skill with id {skill_id} doesn't exists",
    ) as record:
        if skill_id == 1:
            warnings_num = 1
        else:
            warnings_num = 2
        skill: skill_model | None = crud.get_skill_by_id(
            session=get_db_session, skill_id=skill_id
        )
        crud.delete_skill(session=get_db_session, skill=skill)
        assert crud.get_skill_by_id(session=get_db_session, skill_id=skill_id) is None

        if not record:
            pytest.fail("Expected warning was not raised")

        assert len(record) == warnings_num


def test_update_skill_name(
    get_db_session: Session, get_skill_id: int, skill_2: skill_base_schema
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


def test_update_skill_level_of_confidence(
    get_db_session: Session, get_skill_id: int, skill_2: skill_base_schema
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
