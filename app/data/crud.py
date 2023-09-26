"""CRUD functions."""
import sqlite3
from collections.abc import Sequence

import sqlalchemy
from loguru import logger
from sqlalchemy import orm, exc

from app.models.type_aliases import level_of_confidence, skill_base_schema, skill_model


def get_skill_by_id(session: orm.Session, skill_id: int) -> skill_model | None:
    stmt = sqlalchemy.select(skill_model).where(skill_model.skill_id == skill_id)
    skill = session.scalars(statement=stmt).one_or_none()
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exists", stacklevel=2)
    logger.info("Operation 'get_skill_by_id' ended successfully")
    return skill


def get_skill_by_name(session: orm.Session, skill_name: str) -> skill_model | None:
    stmt: sqlalchemy.Select[tuple[skill_model]] = sqlalchemy.select(skill_model).where(
        skill_model.skill_name == skill_name
    )
    skill = session.scalars(stmt).one_or_none()
    if skill is None:
        logger.warning(f"The skill named {skill_name} doesn't exists", stacklevel=2)
    logger.info("Operation 'get_skill_by_name' ended successfully")
    return skill


def create_skill(session: orm.Session, skill: skill_base_schema) -> None:
    try:
        skill_db = skill_model(**skill.model_dump())
        session.add(skill_db)
        session.commit()
        session.refresh(skill_db)
    except exc.IntegrityError:
        logger.exception(f"Skill {skill.skill_name} already exist")
        session.rollback()


def get_skills(session: orm.Session) -> Sequence[skill_model]:
    stmt: sqlalchemy.Select[skill_model] = sqlalchemy.Select(skill_model)
    skills: Sequence[skill_model] = session.scalars(stmt).all()
    return skills


def delete_skill(session: orm.Session, skill: skill_model) -> None:
    if skill:
        session.delete(skill)
        session.commit()


def update_skill_name(session: orm.Session, skill_id: int, new_name: str) -> None:
    session.execute(
        statement=sqlalchemy.update(table=skill_model),
        params={"skill_id": skill_id, "skill_name": new_name},
    )
    session.commit()


def update_skill_level_of_confidence(
    session: orm.Session, skill_id: int, new_level: level_of_confidence
) -> None:
    session.execute(
        statement=sqlalchemy.update(table=skill_model),
        params={"skill_id": skill_id, "level_of_confidence": new_level},
    )
    session.commit()
