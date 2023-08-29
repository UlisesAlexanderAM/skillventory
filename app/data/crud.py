"""CRUD functions"""
from collections.abc import Sequence
import sqlite3
import sqlalchemy
from sqlalchemy import orm

from app.models import schemas, models


def create_skill(session: orm.Session, skill: schemas.Skill):
    if (
        session.scalar(
            sqlalchemy.select(models.Skill.skill_name).where(
                models.Skill.skill_name == skill.skill_name
            )
        )
        is not None
    ):
        raise sqlite3.IntegrityError("The skill already exist")
    skill_db = models.Skill(**skill.model_dump())
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)


def get_skills(session: orm.Session) -> Sequence[models.Skill]:
    stmt: sqlalchemy.Select[models.Skill] = sqlalchemy.Select(models.Skill)
    skills: Sequence[models.Skill] = session.scalars(stmt).all()
    return skills
