"""CRUD functions."""

from collections.abc import Sequence

import sqlalchemy
from loguru import logger
import sqlmodel
from sqlalchemy import exc

from app.models.type_aliases import level_of_confidence, skill_base_model, skill_model

logger.add("test.log")


def get_skill_by_id(session: sqlmodel.Session, skill_id: int) -> skill_model | None:
    with session:
        skill = session.exec(
            sqlmodel.select(skill_model).where(skill_model.skill_id == skill_id)
        ).one_or_none()
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exists", stacklevel=2)
    logger.info("Operation 'get_skill_by_id' ended successfully")
    return skill


def get_skill_by_name(session: sqlmodel.Session, skill_name: str):
    skill = None
    with session:
        skill = session.exec(
            sqlmodel.select(skill_model).where(
                sqlmodel.col(skill_model.skill_name) == skill_name
            )
        ).one_or_none()
    if skill is None:
        logger.warning(f"The skill named {skill_name} doesn't exists", stacklevel=2)
    logger.info("Operation 'get_skill_by_name' ended successfully")
    return skill


def create_skill(session: sqlmodel.Session, skill: skill_base_model) -> None:
    try:
        skill_db = skill_model(**skill.model_dump())
        with session:
            session.add(skill_db)
            session.commit()
            session.refresh(skill_db)
        logger.info(f"Skill {skill.skill_name} created successfully")
    except exc.IntegrityError:
        logger.error(f"Skill {skill.skill_name} already exist")
        session.rollback()


def get_skills(session: sqlmodel.Session) -> Sequence[skill_model]:
    stmt: sqlalchemy.Select[skill_model] = sqlalchemy.Select(skill_model)
    skills: Sequence[skill_model] = session.scalars(stmt).all()
    logger.info("Operation 'get_skills' ended successfully")
    return skills


def delete_skill(session: sqlmodel.Session, skill: skill_model) -> None:
    if skill:
        session.delete(skill)
        session.commit()
        logger.info(f"Skill {skill.skill_name} deleted successfully")


def update_skill_name(session: sqlmodel.Session, skill_id: int, new_name: str) -> None:
    skill = get_skill_by_id(session=session, skill_id=skill_id)
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exist")
    else:
        logger.info(f"Changing the name of {skill.skill_name} to {new_name}")
        with session:
            skill.skill_name = new_name
            session.add(skill)
            session.commit()
            session.refresh(skill)
        logger.info("Skill name changed successfully")


def update_skill_level_of_confidence(
    session: sqlmodel.Session, skill_id: int, new_level: level_of_confidence
) -> None:
    skill = get_skill_by_id(session=session, skill_id=skill_id)
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exist")
    else:
        logger.info(f"Changing the level of {skill.skill_name} to {new_level}")
        with session:
            skill.level_of_confidence = new_level
            session.add(skill)
            session.commit()
            session.refresh(skill)
        logger.info("Skill level changed successfully")
