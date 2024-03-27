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
from typing import Optional, ClassVar, Dict
import sqlmodel


class LevelOfConfidence(enum.Enum):
    """Levels of confidence that the user have in a skill/knowledge"""

    LEVEL_1 = "Inicio del aprendizaje/desarrollo pendiente"
    LEVEL_2 = "Estoy aprendiendo o desarrollando"
    LEVEL_3 = "Tengo confianza, pero el cielo es el limite"


class SkillBase(sqlmodel.SQLModel):
    """Base model of a skill"""

    skill_name: str
    level_of_confidence: LevelOfConfidence

    model_config: ClassVar[Dict[str, Dict[str, list[Dict[str, str]]]]] = {
        "json_schema_extra": {
            "examples": [
                {
                    "skill_name": "Skill",
                    "level_of_confidence": "Inicio del aprendizaje/desarrollo pendiente",
                },
                {
                    "skill_name": "Skill",
                    "level_of_confidence": "Estoy aprendiendo o desarrollando",
                },
                {
                    "skill_name": "Skill",
                    "level_of_confidence": "Tengo confianza, pero el cielo es el limite",
                },
            ]
        }
    }


class Skill(sqlmodel.SQLModel, table=True):
    skill_id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    skill_name: str = sqlmodel.Field(unique=True, index=True)
    level_of_confidence: LevelOfConfidence = sqlmodel.Field(index=True)
