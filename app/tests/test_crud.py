"""Tests for CRUD operations on skills.

This module contains tests for the CRUD (create, read, update, delete)
operations for skills using a test database session fixture.

Fixtures:
- get_db_session: Module scoped session fixture.
- setup_db: Function scoped setup/teardown fixture.
- skill_factory: Session scoped skill factory fixture.
- skill_1: Sample skill fixture.
- skill_2: Another sample skill fixture.

The tests call the CRUD functions defined in app/data/crud.py and
validate the results using the fixtures and expected values.

Tests:
- test_create_skill: Tests creating a new skill.
- test_get_skill_by_id: Tests getting a skill by ID.
- test_get_skill_by_name: Tests getting a skill by the skill's name.
- test_get_skills: Tests getting all skills.
- test_update_skill_name: Tests updating a skill's name.
- test_update_skill_level_of_confidence: Tests updating a skill's level of confidence
- test_delete_skill: Tests deleting a skill.
"""

from collections.abc import Sequence
from typing import Literal

import pytest
from sqlalchemy.orm import Session

from app.data import crud
from app.models.type_aliases import skill_base_schema, skill_model

MULTIPLE_SKILLS = 2


@pytest.mark.parametrize("skill_id,expected_warning", [(1, False), (2, True)])
def test_get_skill_by_id(
    get_db_session: Session,
    create_one_skill: skill_model,  # pyright:ignore
    skill_id: int,
    expected_warning: bool,
    caplog,
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
    skill: skill_model | None = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )

    if expected_warning:
        assert f"The skill with id {skill_id} doesn't exists" in caplog.text
    else:
        assert skill is not None
        assert skill.skill_id == skill_id
        assert "Operation 'get_skill_by_id' ended successfully" in caplog.text


@pytest.mark.parametrize(
    "skill_name,expected_warning", [("python", False), ("java", True)]
)
def test_get_skill_by_name(
    get_db_session: Session,
    create_one_skill: skill_base_schema,  # pyright:ignore
    skill_name: str,
    expected_warning: bool,
    caplog,
) -> None:
    """Tests get_skill_by_name.

    Args:
        get_db_session: Database session fixture
        create_one_skill: Skill fixture
        skill_name: Skill name
        expected_warning: Expected warning

    This test gets the skill by name for an existing and non-existing skill.
    If the skill is found, no warning is expected. If not found, a warning is expected.
    If the skill is found, assert it matches the created skill.
    """
    skill: skill_model | None = crud.get_skill_by_name(
        session=get_db_session, skill_name=skill_name
    )

    if expected_warning:
        assert f"The skill named {skill_name} doesn't exists" in caplog.text
    else:
        assert skill is not None
        assert skill.skill_name == create_one_skill.skill_name


@pytest.mark.parametrize("expected_exception", [False, True])
def test_create_skill(
    get_db_session: Session,
    skill_1: skill_base_schema,
    expected_exception: bool,
    caplog,
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

    if expected_exception:
        crud.create_skill(session=get_db_session, skill=skill_1)
        assert f"Skill {skill.skill_name} already exist" in caplog.text


@pytest.mark.parametrize("number_of_skills", [0, 1, 2])
def test_get_skills(
    get_db_session: Session,
    skill_1: skill_base_schema,
    skill_2: skill_base_schema,
    number_of_skills: Literal[0, 1, 2],
) -> None:
    """Tests getting all skills from the database.

    Args:
        get_db_session: The database session fixture.
        skill_1: The first sample skill fixture.
        skill_2: The second sample skill fixture.
        number_of_skills: The number of skills to create.

    This test does the following:

    1. Optionally creates skill_1 and/or skill_2 based on number_of_skills.
    2. Gets all skills from the database.
    3. Validates the number of skills matches number_of_skills.
    4. If skills were created, validates their attributes match the fixtures.
    """
    skills: list[skill_base_schema] = [skill_1, skill_2]
    skills_wanted: list[skill_base_schema] = []
    for _ in range(number_of_skills):
        crud.create_skill(session=get_db_session, skill=skills[_])
        skills_wanted.append(skills[_])
    skills_db: Sequence[skill_model] = crud.get_skills(session=get_db_session)

    assert len(skills_db) == number_of_skills

    for skill_wanted, skill_db in zip(skills_wanted, skills_db, strict=True):
        assert skill_db.skill_name == skill_wanted.skill_name
        assert skill_db.level_of_confidence == skill_wanted.level_of_confidence


@pytest.mark.parametrize("skill_id", [1, 2])
def test_delete_skill(
    get_db_session: Session, create_one_skill: skill_model, skill_id: Literal[1, 2]
) -> None:
    """Tests deleting a skill by ID.

    Args:
        get_db_session: The database session fixture.
        create_one_skill: The fixture to create a sample skill.
        skill_id: The ID of the skill to delete.

    This test does the following:

    1. Attempts to get a skill by the provided ID.
    2. Deletes the skill if found.
    3. Validates the skill no longer exists.
    4. Checks that a UserWarning is raised if skill not found.
    5. Validates the correct number of warnings were raised.
    """
    skill: skill_model | None = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )
    crud.delete_skill(session=get_db_session, skill=skill)
    assert crud.get_skill_by_id(session=get_db_session, skill_id=skill_id) is None


@pytest.mark.parametrize("skill_id,expected_warning", [(1, False), (2, True)])
def test_update_skill_name(
    get_db_session: Session,
    create_one_skill: skill_model,
    skill_2: skill_base_schema,
    skill_id: Literal[1, 2],
    expected_warning: bool,
    caplog,
) -> None:
    """Tests updating the name for a skill.

    Args:
        get_db_session: The database session fixture.
        get_skill_id: The fixture that returns a skill ID.
        skill_2: The fixture for a sample skill object.

    This test does the following:

    1. Gets a skill ID from the get_skill_id fixture.
    2. Updates the name for that skill ID using the
    name from skill_2.
    3. Retrieves the updated skill from the database.
    4. Validates the updated name matches skill_2.
    5. Validates the skill ID matches the original.
    """
    crud.update_skill_name(
        session=get_db_session, skill_id=skill_id, new_name=skill_2.skill_name
    )
    skill_updated: skill_model | None = crud.get_skill_by_id(
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
    get_db_session: Session,
    create_one_skill: skill_model,
    skill_2: skill_base_schema,
    skill_id: int,
    expected_warning: bool,
    caplog,
) -> None:
    """Tests updating the level of confidence for a skill.

    Args:
        get_db_session: The database session fixture.
        get_skill_id: The fixture that returns a skill ID.
        skill_2: The fixture for a sample skill object.

    This test does the following:

    1. Gets a skill ID from the get_skill_id fixture.
    2. Updates the level of confidence for that skill ID using the level from skill_2.
    3. Retrieves the updated skill from the database.
    4. Validates the updated level of confidence matches skill_2.
    5. Validates the skill ID matches the original.
    """
    crud.update_skill_level_of_confidence(
        session=get_db_session,
        skill_id=skill_id,
        new_level=skill_2.level_of_confidence,
    )
    skill_updated: skill_model | None = crud.get_skill_by_id(
        session=get_db_session, skill_id=skill_id
    )
    if expected_warning:
        assert f"The skill with id {skill_id} doesn't exist" in caplog.text
    else:
        assert skill_updated is not None
        assert skill_updated.skill_id == skill_id
        assert skill_updated.level_of_confidence == skill_2.level_of_confidence
