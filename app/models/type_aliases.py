from typing import TypeAlias

from app.models import schemas, models

skill_base_schema: TypeAlias = schemas.SkillBase
skill_schema: TypeAlias = schemas.Skill
place_with_greater_interest_base_schema: TypeAlias = (
    schemas.PlaceWithGreaterInterestBase
)
place_with_greater_interest_schema: TypeAlias = schemas.PlaceWithGreaterInterest

skill_model: TypeAlias = models.Skill
place_with_greater_interest_model: TypeAlias = models.PlaceWithGreaterInterest

level_of_confidence: TypeAlias = schemas.LevelOfConfidence
