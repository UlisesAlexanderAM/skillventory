"""Defines the SQLAlchemy models"""

import sqlalchemy
from sqlalchemy import orm

from app.database import config
from app.models import schemas

skill_place_table = sqlalchemy.Table(
    "skill_place_table",
    config.Base.metadata,
    sqlalchemy.Column("skill_id", sqlalchemy.ForeignKey("skill.id"), primary_key=True),
    sqlalchemy.Column(
        "place_id",
        sqlalchemy.ForeignKey("places_with_greater_interest.id"),
        primary_key=True,
    ),
)


class Skill(config.Base):
    """Model of the table skill"""

    __tablename__: str = "skill"

    skill_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    skill_name: orm.Mapped[str] = orm.mapped_column(
        unique=True, nullable=False, index=True
    )
    level_of_confidence: orm.Mapped[schemas.LevelOfConfidence] = orm.mapped_column(
        nullable=False, index=True
    )
    places: orm.Mapped[list["PlaceWithGreaterInterest"]] = orm.relationship(
        secondary=skill_place_table, back_populates="places"
    )


class PlaceWithGreaterInterest(config.Base):
    """Model of the table place_with_greater_interest"""

    __tablename__: str = "place_with_greater_interest"

    place_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    place_name: orm.Mapped[str] = orm.mapped_column(
        unique=True, nullable=False, index=True
    )
    website_link: orm.Mapped[str] = orm.mapped_column(nullable=False)
    job_postings_link: orm.Mapped[str]
    linkedin_link: orm.Mapped[str]
    skills: orm.Mapped[list["Skill"]] = orm.relationship(
        secondary=skill_place_table, back_populates="skills"
    )
