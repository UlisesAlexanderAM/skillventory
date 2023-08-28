"""CRUD functions"""
from collections.abc import Sequence
import sqlalchemy
from sqlalchemy import orm

from app.models import schemas, models


def create_skill(session: orm.Session, skill: schemas.Skill):
    skill_db = models.Skill(**skill.model_dump())
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)


def get_skills(session: orm.Session) -> Sequence[models.Skill]:
    stmt: sqlalchemy.Select[models.Skill] = sqlalchemy.Select(models.Skill)
    skills: Sequence[models.Skill] = session.scalars(stmt).all()
    return skills
