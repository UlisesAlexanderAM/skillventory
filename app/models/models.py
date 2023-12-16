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

import enum
from typing import Optional
import sqlmodel
import pydantic


class LevelOfConfidence(enum.Enum):
    """Enum of the level of confidence."""

    LEVEL_1 = "Debo empezar a aprender o desarrollar"
    LEVEL_2 = "Estoy aprendiendo o desarrollando"
    LEVEL_3 = "Tengo confianza"


class SkillBase(sqlmodel.SQLModel):
    """SkillBase Pydantic model.

    Attributes:
        skill_name: The name of the skill.
        level_of_confidence: The level of confidence for the skill.

    This model defines the base fields for a Skill using Pydantic.
    It is used as a base for the Skill schema model.
    """

    skill_name: str
    level_of_confidence: LevelOfConfidence


class PlaceWithGreaterInterestBase(sqlmodel.SQLModel):
    """PlaceWithGreaterInterestBase Pydantic model.

    Attributes:
        place_name: The name of the place.
        website_link: The website link for the place.
        job_postings_link: Optional job postings link.
        linkedin_link: Optional LinkedIn link.

    This model defines the base fields for a PlaceWithGreaterInterest
    using Pydantic. It is used as a base for the PlaceWithGreaterInterest
    schema model.
    """

    place_name: str
    website_link: pydantic.HttpUrl
    job_postings_link: Optional[pydantic.HttpUrl]
    linkedin_link: Optional[pydantic.HttpUrl]


class DomainBase(sqlmodel.SQLModel):
    domain_name: str


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
    skill_name: str = sqlmodel.Field(unique=True, index=True)
    level_of_confidence: LevelOfConfidence = sqlmodel.Field(index=True)
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
    place_name: str = sqlmodel.Field(unique=True, index=True)
    website_link: str
    job_postings_link: Optional[str] = sqlmodel.Field(default=None)
    linkedin_link: Optional[str] = sqlmodel.Field(default=None)
    # skills: orm.Mapped[list["Skill"]] = orm.relationship(
    #     secondary=skill_place_table, back_populates="places"
    # )


class Domain(sqlmodel.SQLModel):
    domain_id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    domain_name: str = sqlmodel.Field(unique=True, index=True)

    # skills: orm.Mapped[list["Skill"]] = orm.relationship(
    #     secondary=skill_domain_table, back_populates="domains"
    # )
