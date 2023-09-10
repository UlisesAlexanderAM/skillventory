"""Defines the pydantic models."""

import enum
import pydantic
from typing import Optional


class LevelOfConfidence(enum.Enum):
    """Enum of the level of confidence."""

    LEVEL_1 = "Debo empezar a aprender o desarrollar"
    LEVEL_2 = "Estoy aprendiendo o desarrollando"
    LEVEL_3 = "Tengo confianza"


class SkillBase(pydantic.BaseModel):
    """Model of the skill/knowledge/competence."""

    skill_name: str
    level_of_confidence: LevelOfConfidence

    model_config = pydantic.ConfigDict(from_attributes=True)


class PlaceWithGreaterInterestBase(pydantic.BaseModel):
    """Model of the place with greater interest."""

    place_name: str
    website_link: pydantic.HttpUrl
    job_postings_link: Optional[pydantic.HttpUrl]
    linkedin_link: Optional[pydantic.HttpUrl]


class Skill(SkillBase):
    skill_id: int
    places: list[PlaceWithGreaterInterestBase]

    model_config = pydantic.ConfigDict(from_attributes=True)


class PlaceWithGreaterInterest(PlaceWithGreaterInterestBase):
    place_id: int
    skills: list[SkillBase]

    model_config = pydantic.ConfigDict(from_attributes=True)
