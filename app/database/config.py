"""Database configuration"""

import sqlalchemy
import pydantic_settings
from sqlalchemy import orm, pool


class DBSettings(pydantic_settings.BaseSettings):
    """Pydantic model to store the sqlite url.
    If the environment variable is not set uses 'sqlite:///./database.db'"""

    SQLITE_URL: str = "sqlite:///./database.db"

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")


db_settings = DBSettings()

engine: sqlalchemy.Engine = sqlalchemy.create_engine(
    url=db_settings.SQLITE_URL, echo=True, connect_args={"check_same_thread": False}
)

LocalSession = orm.sessionmaker(autoflush=False, bind=engine)

Base = orm.declarative_base()


class DBTestingSettings(pydantic_settings.BaseSettings):
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
