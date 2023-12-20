"""Module that defines the routes related to skills/knowledge/competence."""

from collections.abc import Sequence
from typing import Annotated, Dict, Optional

import fastapi as fa
import sqlmodel
from fastapi import responses

from app.data import crud
from app.data import dependencies as deps
from app.models import models

router: fa.APIRouter = fa.APIRouter(
    prefix="/skills",
    tags=["Skills"],
    responses={404: {"description": "Skill not found"}},
)


@router.get(
    "/", status_code=fa.status.HTTP_200_OK, response_model=Sequence[models.Skill]
)
def get_skills(
    session: Annotated[sqlmodel.Session, fa.Depends(deps.get_db_session)],
    response: fa.Response,
) -> Sequence[models.Skill]:
    skills = crud.get_skills(session=session)
    response.headers["X-Total-Count"] = str(len(skills))
    response.headers["X-Offset"] = "0"
    response.headers["X-Limit"] = "15"
    response.headers["X-Total-Pages"] = "1"
    if len(skills) == 16:  # noqa
        response.headers["X-Total-Pages"] = "2"
    return skills


@router.post(
    "/",
    status_code=fa.status.HTTP_201_CREATED,
    responses={409: {"description": "Conflicting request"}},
    response_class=responses.JSONResponse,
)
def post_skill(
    session: Annotated[sqlmodel.Session, fa.Depends(deps.get_db_session)],
    skill: Annotated[models.SkillBase, fa.Body(description="Skill to add to the DB.")],
) -> Dict[str, str]:
    if not crud.get_skill_by_name(session=session, skill_name=skill.skill_name):
        crud.create_skill(session=session, skill=skill)
        return {"message": "Skill added successfully"}
    raise fa.HTTPException(
        status_code=fa.status.HTTP_409_CONFLICT, detail="Skill already added"
    )


@router.get(
    "/id/{skill_id}", status_code=fa.status.HTTP_200_OK, response_model=models.Skill
)
def get_skill_by_id(
    session: Annotated[sqlmodel.Session, fa.Depends(deps.get_db_session)],
    skill_id: Annotated[int, fa.Path(title="The ID of the skill to get")],
) -> models.Skill:
    skill_db: Optional[models.Skill] = crud.get_skill_by_id(
        session=session, skill_id=skill_id
    )
    if skill_db is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail=f"Skill with id {skill_id} not found",
        )
    return skill_db


@router.get(
    "/name/{skill_name}", status_code=fa.status.HTTP_200_OK, response_model=models.Skill
)
def get_skill_by_name(
    session: Annotated[sqlmodel.Session, fa.Depends(deps.get_db_session)],
    skill_name: Annotated[str, fa.Path(title="The name of the skill to get")],
) -> Optional[models.Skill]:
    skill_db: Optional[models.Skill] = crud.get_skill_by_name(
        session=session, skill_name=skill_name
    )
    if skill_db is None:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail=f"Skill with name '{skill_name}' not found",
        )
    return skill_db
