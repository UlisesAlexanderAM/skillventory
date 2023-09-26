import enum
import pydantic
from typing import Optional


class LevelOfConfidence(enum.Enum):
    """Enum of the level of confidence."""

    LEVEL_1 = "Debo empezar a aprender o desarrollar"
    LEVEL_2 = "Estoy aprendiendo o desarrollando"
    LEVEL_3 = "Tengo confianza"


class SkillBase(pydantic.BaseModel):
    """SkillBase Pydantic model.

    Attributes:
        skill_name: The name of the skill.
        level_of_confidence: The level of confidence for the skill.

        model_config: Model configuration from attributes.
        Allows to access the values of the attributes
        using dot notations.

    This model defines the base fields for a Skill using Pydantic.
    It is used as a base for the Skill schema model.
    """

    skill_name: str
    level_of_confidence: LevelOfConfidence

    model_config = pydantic.ConfigDict(from_attributes=True)


class PlaceWithGreaterInterestBase(pydantic.BaseModel):
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

    model_config = pydantic.ConfigDict(from_attributes=True)


class DomainBase(pydantic.BaseModel):
    domain_name: str

    model_config = pydantic.ConfigDict(from_attributes=True)


class Skill(SkillBase):
    """Skill Pydantic model.

    Attributes:
        skill_id: The ID of the skill.
        places: Related places for the skill.

        model_config: Model configuration from attributes.
        Allows to access the values of the attributes
        using dot notations.

    This model defines a complete Skill schema, extending SkillBase.
    It adds the skill ID and related places fields.
    """

    skill_id: int
    places: list[PlaceWithGreaterInterestBase]
    domains: list[DomainBase]

    model_config = pydantic.ConfigDict(from_attributes=True)


class PlaceWithGreaterInterest(PlaceWithGreaterInterestBase):
    """PlaceWithGreaterInterest Pydantic model.

    Attributes:
        place_id: The ID of the place.
        skills: Related skills for the place.

        model_config: Model configuration from attributes.
        Allows to access the values of the attributes
        using dot notations.

    This model defines a complete PlaceWithGreaterInterest schema,
    extending PlaceWithGreaterInterestBase.

    It adds the place ID and related skills fields.
    """

    place_id: int
    skills: list[SkillBase]

    model_config = pydantic.ConfigDict(from_attributes=True)


class Domain(DomainBase):
    domain_id: int

    model_config = pydantic.ConfigDict(from_attributes=True)
