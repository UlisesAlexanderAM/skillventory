"""Type aliases for models and schemas.

This module contains type aliases for models and schemas to improve type hinting
and avoid circular imports.

Aliases:

- skill_base_schema: Alias for SkillBase schema.
- skill_schema: Alias for Skill schema.
- place_with_greater_interest_base_schema: Alias for PlaceWithGreaterInterestBase schema.
- place_with_greater_interest_schema: Alias for PlaceWithGreaterInterest schema.
- skill_model: Alias for Skill model.
- place_with_greater_interest_model: Alias forPlaceWithGreaterInterest model.
- level_of_confidence: Alias for LevelOfConfidence enum.

Using these aliases improves code completion, clarity, and avoids circular
imports between the models and schemas modules.
"""
from typing import TypeAlias

from app.models import schemas, models

skill_base_schema: TypeAlias = schemas.SkillBase
skill_schema: TypeAlias = models.Skill
place_with_greater_interest_base_schema: TypeAlias = (
    schemas.PlaceWithGreaterInterestBase
)
place_with_greater_interest_schema: TypeAlias = models.PlaceWithGreaterInterest
skill_model: TypeAlias = models.Skill
place_with_greater_interest_model: TypeAlias = models.PlaceWithGreaterInterest

level_of_confidence: TypeAlias = schemas.LevelOfConfidence
