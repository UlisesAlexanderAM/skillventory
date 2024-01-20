"""CRUD functions."""

from collections.abc import Sequence
from typing import Optional

import sqlmodel
from loguru import logger
from sqlalchemy import exc

from app.models import models


def get_skill_by_id(session: sqlmodel.Session, skill_id: int) -> Optional[models.Skill]:
    skill: Optional[models.Skill] = session.get(models.Skill, skill_id)
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exists", stacklevel=2)
    logger.info("Operation 'get_skill_by_id' ended successfully")
    return skill


def get_skill_by_name(
    session: sqlmodel.Session, skill_name: str
) -> Optional[models.Skill]:
    statement = sqlmodel.select(models.Skill).where(
        sqlmodel.col(models.Skill.skill_name) == skill_name
    )
    results = session.exec(statement=statement)
    skill: Optional[models.Skill] = results.first()
    if skill is None:
        logger.warning(f"The skill named {skill_name} doesn't exists", stacklevel=2)
    logger.info("Operation 'get_skill_by_name' ended successfully")
    return skill


def create_skill(session: sqlmodel.Session, skill: models.SkillBase) -> None:
    try:
        skill_db: models.Skill = models.Skill(**skill.model_dump())
        session.add(skill_db)
        session.commit()
        session.refresh(skill_db)
        logger.info(f"Skill {skill.skill_name} created successfully")
    except exc.IntegrityError:
        logger.error(f"Skill {skill.skill_name} already exist")
        session.rollback()


def get_skills(
    session: sqlmodel.Session, offset: int = 0, limit: int = 15
) -> Sequence[models.Skill]:
    statement = sqlmodel.select(models.Skill).offset(offset).limit(limit)
    results = session.exec(statement)
    skills = results.all()
    logger.info("Operation 'get_skills' ended successfully")
    return skills


def delete_skill(session: sqlmodel.Session, skill: Optional[models.Skill]) -> None:
    if skill:
        session.delete(skill)
        session.commit()
        logger.info(f"Skill {skill.skill_name} deleted successfully")


def update_skill_name(session: sqlmodel.Session, skill_id: int, new_name: str) -> None:
    skill: Optional[models.Skill] = get_skill_by_id(session=session, skill_id=skill_id)
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exist")
    else:
        logger.info(f"Changing the name of {skill.skill_name} to {new_name}")
        skill.skill_name = new_name
        session.add(skill)
        session.commit()
        session.refresh(skill)
        logger.info("Skill name changed successfully")


def update_skill_level_of_confidence(
    session: sqlmodel.Session, skill_id: int, new_level: models.LevelOfConfidence
) -> None:
    skill: Optional[models.Skill] = get_skill_by_id(session=session, skill_id=skill_id)
    if skill is None:
        logger.warning(f"The skill with id {skill_id} doesn't exist")
    else:
        logger.info(f"Changing the level of {skill.skill_name} to {new_level}")
        skill.level_of_confidence = new_level
        session.add(skill)
        session.commit()
        session.refresh(skill)
        logger.info("Skill level changed successfully")
