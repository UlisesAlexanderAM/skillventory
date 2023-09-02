"""CRUD functions"""
from collections.abc import Sequence
import sqlite3
import sqlalchemy
from sqlalchemy import orm

from app.models import schemas, models


def get_skill_by_id(session: orm.Session, skill_id: int) -> models.Skill | None:
    stmt = sqlalchemy.select(models.Skill).where(models.Skill.skill_id == skill_id)
    return session.scalars(statement=stmt).one_or_none()


def get_skill_by_name(session: orm.Session, skill_name: str) -> models.Skill | None:
    stmt: sqlalchemy.Select[tuple[models.Skill]] = sqlalchemy.select(
        models.Skill
    ).where(models.Skill.skill_name == skill_name)
    return session.scalars(stmt).one_or_none()


def create_skill(session: orm.Session, skill: schemas.SkillBase) -> None:
    if get_skill_by_name(session=session, skill_name=skill.skill_name) is not None:
        raise sqlite3.IntegrityError("The skill already exist")
    skill_db = models.Skill(**skill.model_dump())
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)


def get_skills(session: orm.Session) -> Sequence[models.Skill]:
    stmt: sqlalchemy.Select[models.Skill] = sqlalchemy.Select(models.Skill)
    skills: Sequence[models.Skill] = session.scalars(stmt).all()
    return skills


def delete_skill(session: orm.Session, skill: models.Skill) -> None:
    if skill:
        session.delete(skill)
        session.commit()


def update_skill_name(session: orm.Session, skill_id: int, new_name: str) -> None:
    session.execute(
        sqlalchemy.update(models.Skill),
        {"skill_id": skill_id, "skill_name": new_name},
    )
    session.commit()
