"""Module that defines the routes related to skills/knowledge/competence."""

from collections.abc import Sequence
from typing import Annotated, Any, Dict, Optional

import fastapi as fa
import sqlmodel
from fastapi import responses, status

from app.data import crud
from app.data import dependencies as deps
from app.models import models

router: fa.APIRouter = fa.APIRouter(
    prefix="/skills",
    tags=["Skills"],
    responses={404: {"description": "Skill not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Sequence[models.Skill])
def get_skills(
    session: Annotated[sqlmodel.Session, fa.Depends(deps.get_db_session)],
    response: fa.Response,
    limit: Annotated[int, fa.Query()] = 15,
    offset: Annotated[int, fa.Query()] = 0,
) -> Sequence[models.Skill]:
    (skills, count) = crud.get_skills(session=session, offset=offset, limit=limit)
    response.headers["X-Total-Count"] = str(count)
    response.headers["X-Offset"] = str(offset)
    response.headers["X-Limit"] = str(limit)
    return skills


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
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
        status_code=status.HTTP_409_CONFLICT, detail="Skill already added"
    )


@router.get(
    "/id/{skill_id}", status_code=status.HTTP_200_OK, response_model=models.Skill
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with id {skill_id} not found",
        )
    return skill_db


@router.get(
    "/name/{skill_name}", status_code=status.HTTP_200_OK, response_model=models.Skill
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with name '{skill_name}' not found",
        )
    return skill_db


@router.patch(
    "/{skill_id}", status_code=status.HTTP_200_OK, response_model=models.Skill
)
def update_skill(
    session: Annotated[sqlmodel.Session, fa.Depends(deps.get_db_session)],
    skill_id: Annotated[int, fa.Path(title="ID of the skill to update")],
    skill: Annotated[
        models.SkillBase,
        fa.Body(title="Body of the modified skill"),
    ],
) -> Any:
    skill_to_update = crud.get_skill_by_id(session=session, skill_id=skill_id)
    if skill_to_update is None:
        raise fa.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with Id {skill_id} not found",
        )
    skill_name_received = skill.skill_name
    skill_level_received = skill.level_of_confidence
    crud.update_skill_if_changed(
        session=session,
        skill=skill_to_update,
        skill_name=skill_name_received,
        skill_level=skill_level_received,
    )
    return crud.get_skill_by_id(session=session, skill_id=skill_id)
