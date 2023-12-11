"""Database models.

This module defines the SQLAlchemy models for the database using
the declarative base from app.database.config.

Models:

- Skill: Maps to skill table.
- PlaceWithGreaterInterest: Maps to place_with_greater_interest table.

The models have columns mapped to the corresponding database tables.
Relationships between models are defined using SQLAlchemy relationships
and association tables.

This allows usage of the models for CRUD operations in SQLAlchemy
and for serialization/deserialization with Pydantic.
"""
from typing import Optional
import sqlmodel

from app.models import schemas

# skill_place_table = sqlalchemy.Table(
#     "skill_place_table",
#     config.Base.metadata,
#     sqlalchemy.Column(
#         "skill_id",
#         sqlalchemy.Integer,
#         sqlalchemy.ForeignKey(column="skill.skill_id"),
#         primary_key=True,
#     ),
#     sqlalchemy.Column(
#         "place_id",
#         sqlalchemy.Integer,
#         sqlalchemy.ForeignKey(column="place_with_greater_interest.place_id"),
#         primary_key=True,
#     ),
# )

# skill_domain_table = sqlalchemy.Table(
#     "skill_domain_table",
#     config.Base.metadata,
#     sqlalchemy.Column(
#         "skill_id",
#         sqlalchemy.Integer,
#         sqlalchemy.ForeignKey(column="skill.skill_id"),
#         primary_key=True,
#     ),
#     sqlalchemy.Column(
#         "domain_id",
#         sqlalchemy.Integer,
#         sqlalchemy.ForeignKey(column="domain.domain_id"),
#         primary_key=True,
#     ),
# )


class Skill(sqlmodel.SQLModel, table=True):
    """Skill SQLModel model.

    Attributes:
        skill_id: Primary key.
        skill_name: Skill name.
        level_of_confidence: Skill confidence level.
        places: Places related to skill.

    This model defines a Skill with columns mapped to the skill
    database table.

    The relationship to PlaceWithGreaterInterest is defined using
    the intermediate table skill_place_table.
    """

    skill_id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    skill_name: str = sqlmodel.Field(unique=True, nullable=False, index=True)
    level_of_confidence: schemas.LevelOfConfidence = sqlmodel.Field(
        nullable=False, index=True
    )
    # places: orm.Mapped[list["PlaceWithGreaterInterest"]] = orm.relationship(
    #     secondary=skill_place_table, back_populates="skills"
    # )
    # domains: orm.Mapped[list["Domain"]] = orm.relationship(
    #     secondary=skill_domain_table, back_populates="skills"
    # )


class PlaceWithGreaterInterest(sqlmodel.SQLModel):
    """PlaceWithGreaterInterest SQLAlchemy model.

    Attributes:
        place_id: Primary key.
        place_name: Place name.
        website_link: Website link.
        job_postings_link: Job postings link.
        linkedin_link: LinkedIn link.
        skills: Related skills, mapped with secondary table.

    This model defines a PlaceWithGreaterInterest with columns mapped to the
    place_with_greater_interest database table.

    The relationship to Skill is defined using the intermediate table skill_place_table.
    """

    place_id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    place_name: str = sqlmodel.Field(unique=True, nullable=False, index=True)
    website_link: str = sqlmodel.Field(nullable=False)
    job_postings_link: str
    linkedin_link: str
    # skills: orm.Mapped[list["Skill"]] = orm.relationship(
    #     secondary=skill_place_table, back_populates="places"
    # )


class Domain(sqlmodel.SQLModel):
    domain_id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    domain_name: str = sqlmodel.Field(unique=True, nullable=False, index=True)

    # skills: orm.Mapped[list["Skill"]] = orm.relationship(
    #     secondary=skill_domain_table, back_populates="domains"
    # )
