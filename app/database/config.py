"""Database configuration."""

import pydantic_settings
from sqlalchemy import pool
import sqlmodel
from sqlmodel import SQLModel


class DBSettings(pydantic_settings.BaseSettings):
    """Database settings model.

    Attributes:
        SQLITE_URL: The URL for the SQLite database. Default is sqlite:///./database.db
        ECHO: True if you want to see all SQL statements printed. Default is False
        model_config: Configuration for Pydantic models loaded from .env file.

    This class defines the database settings by subclassing BaseSettings.
    The SQLITE_URL provides the database URL.

    The model_config tells pydantic to use ".env" as an env file to load settings from.
    """

    SQLITE_URL: str = "sqlite:///./database.db"
    ECHO: bool = False

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")


db_settings = DBSettings()

engine = sqlmodel.create_engine(
    url=db_settings.SQLITE_URL,
    echo=db_settings.ECHO,
    connect_args={"check_same_thread": False},
)


class DBTestingSettings(pydantic_settings.BaseSettings):
    """Database testing settings model.

    Attributes:
        SQLITE_URL: The URL for the SQLite test database. Default is sqlite://
        which is an in-memory database.
        model_config: Configuration for Pydantic models loaded from .env file.

    This class defines the test database settings by subclassing BaseSettings.
    The SQLITE_URL provides the test database URL.

    The model_config tells pydantic to use ".env" as an env file to load settings from
    """

    SQLITE_URL: str = "sqlite://"

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")


db_testing_settings = DBTestingSettings()

testing_engine = sqlmodel.create_engine(
    url=db_testing_settings.SQLITE_URL,
    echo=True,
    poolclass=pool.StaticPool,
    connect_args={"check_same_thread": False},
)


Base = SQLModel


def create_db_and_tables():
    Base.metadata.create_all(engine)
