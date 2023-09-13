"""Database configuration."""

import sqlalchemy
import pydantic_settings
from sqlalchemy import orm, pool


class DBSettings(pydantic_settings.BaseSettings):
    """Database settings model.

    Attributes:
        SQLITE_URL: The URL for the SQLite database. Default is sqlite:///./database.db
        model_config: Configuration for Pydantic models loaded from .env file.

    This class defines the database settings by subclassing BaseSettings.
    The SQLITE_URL provides the database URL.

    The model_config tells pydantic to use ".env" as an env file to load settings from.
    """

    SQLITE_URL: str = "sqlite:///./database.db"

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")


db_settings = DBSettings()

engine: sqlalchemy.Engine = sqlalchemy.create_engine(
    url=db_settings.SQLITE_URL, echo=True, connect_args={"check_same_thread": False}
)

LocalSession = orm.sessionmaker(autoflush=False, bind=engine)

Base = orm.declarative_base()


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

testing_engine = sqlalchemy.create_engine(
    url=db_testing_settings.SQLITE_URL,
    echo=True,
    poolclass=pool.StaticPool,
    connect_args={"check_same_thread": False},
)

TestLocalSession = orm.sessionmaker(autoflush=False, bind=testing_engine)
