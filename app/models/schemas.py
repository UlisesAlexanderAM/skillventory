"""Defines the pydantic models"""

import enum
from typing import Optional
import pydantic


class LevelOfConfidence(enum.Enum):
    LEVEL_1 = "Debo empezar a aprender o desarrollar"
    LEVEL_2 = "Estoy aprendiendo o desarrollando"
    LEVEL_3 = "Tengo confianza"


class Skill(pydantic.BaseModel):
    skill_name: str
    level_of_confidence: LevelOfConfidence


class PlaceWithGreaterInterest(pydantic.BaseModel):
    place_name: str
    website_link: pydantic.HttpUrl
    job_postings_link: Optional[pydantic.HttpUrl]
    linkedin_link: Optional[pydantic.HttpUrl]
