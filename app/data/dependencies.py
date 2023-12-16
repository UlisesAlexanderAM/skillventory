"""Defines the dependencies used."""

from collections.abc import Iterator
import sqlmodel
from contextlib import contextmanager
from app.database import config
from sqlmodel import Session


@contextmanager
def get_db_session() -> Iterator[Session]:
    """Gets a database session object.

    Yields:
        db: The database session.
    """
    db: Session = sqlmodel.Session(config.engine)
    try:
        yield db
    finally:
        db.close()
