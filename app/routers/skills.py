"""Module that defines the routes related to skills/knowledge/competence."""
from typing import Annotated
import fastapi as fa
from fastapi import APIRouter, status
from collections.abc import Sequence
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.data import crud, dependencies as deps
from app.models.type_aliases import skill_schema, skill_model, skill_base_schema


router: APIRouter = fa.APIRouter(
    prefix="/skills",
    tags=["Skills"],
    responses={404: {"description": "Skill not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[skill_schema])
def get_skills(
    session: Annotated[Session, fa.Depends(deps.get_db_session)],
) -> Sequence[skill_model]:
    return crud.get_skills(session=session)
