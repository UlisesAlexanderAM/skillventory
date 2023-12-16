"""Type aliases for models and models.

This module contains type aliases for models and models to improve type hinting
and avoid circular imports.

Aliases:

- skill_base_model: Alias for SkillBase model.
- skill_model: Alias for Skill model.
- place_with_greater_interest_base_model: Alias for PlaceWithGreaterInterestBase model.
- place_with_greater_interest_model: Alias for PlaceWithGreaterInterest model.
- skill_model: Alias for Skill model.
- place_with_greater_interest_model: Alias forPlaceWithGreaterInterest model.
- level_of_confidence: Alias for LevelOfConfidence enum.

Using these aliases improves code completion, clarity.
"""

from typing import TypeAlias

from app.models import models

skill_base_model: TypeAlias = models.SkillBase
skill_model: TypeAlias = models.Skill
place_with_greater_interest_base_model: TypeAlias = models.PlaceWithGreaterInterestBase
place_with_greater_interest_model: TypeAlias = models.PlaceWithGreaterInterest

level_of_confidence: TypeAlias = models.LevelOfConfidence
