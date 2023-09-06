"""Defines the dependencies used"""
from sqlalchemy.orm import Session
from collections.abc import Iterator
from app.database import config


def get_db_session() -> Iterator[Session]:
    """Gets a database session object.

    Yields:
        db: The database session.
    """
    db: Session = config.LocalSession()
    try:
        yield db
    finally:
        db.close()
