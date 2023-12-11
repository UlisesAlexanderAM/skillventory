import enum
import pydantic
from typing import Optional
import sqlmodel


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
