import fastapi
from fastapi import testclient

from app import main
from app.data import dependencies
from tests import conftest

main.app.dependency_overrides[dependencies.get_db_session] = conftest.get_db_session

