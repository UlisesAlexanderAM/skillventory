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


@router.post("/", status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
def post_skill(
    skill: Annotated[skill_base_schema, fa.Body(description="Skill to add to the DB.")],
    session: Annotated[Session, fa.Depends(deps.get_db_session)],
):
    if not crud.get_skill_by_name(session=session, skill_name=skill.skill_name):
        crud.create_skill(session=session, skill=skill)
        return {"message": "Skill added successfully"}
    raise fa.HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="Skill already added"
    )
