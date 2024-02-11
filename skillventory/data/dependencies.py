"""Defines the dependencies used."""

from collections.abc import Iterator

import sqlmodel

from skillventory.database import config


def get_db_session() -> Iterator[sqlmodel.Session]:
    """Gets a database session object.

    Yields:
        session The database session.
    """
    with sqlmodel.Session(config.engine) as session:
        yield session
