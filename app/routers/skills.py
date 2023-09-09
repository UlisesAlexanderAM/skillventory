"""Module that defines the routes related to skills/knowledge/competence"""
import fastapi
from fastapi import status
from fastapi import APIRouter
from collections.abc import Sequence

from app.models.schemas import skill_schema
from app.data import dependencies as deps

router: APIRouter = fastapi.APIRouter(
    prefix="/skills",
    tags=["Skills"],
    responses={404: {"description": "Skill not found"}},
)


# @routers.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[skill_schema])
# def get_skills(session: Session = Depends(deps.get_db_session)):
#     pass
