"""CRUD functions"""
import sqlalchemy
from sqlalchemy import orm

from app.models import schemas, models


def get_skill(skill_name: str):
    pass


def create_skill(session: orm.Session, skill: schemas.Skill):
    skill_db = models.Skill(**skill.model_dump())
    session.add(skill_db)
    session.commit()
    session.refresh(skill_db)
