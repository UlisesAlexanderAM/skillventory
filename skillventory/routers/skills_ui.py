from typing import Annotated

import fastapi
import fastui
import sqlmodel
from fastui import components
from fastui.components import display


from skillventory.data import crud
from skillventory.data import dependencies as deps
from skillventory.models import models

router = fastapi.APIRouter(prefix="/api/skills", tags=["Skills UI"])


@router.get("/", response_model=fastui.FastUI, response_model_exclude_none=True)
def skills_table(
    session: Annotated[sqlmodel.Session, fastapi.Depends(deps.get_db_session)],
    page: Annotated[int, fastapi.Query()] = 1,
    page_size: Annotated[int, fastapi.Query()] = 15,
) -> list[fastui.AnyComponent]:
    skills, total = crud.get_skills(
        session=session, offset=(page - 1) * page_size, limit=page_size
    )
    return [
        components.Page(
            components=[
                components.Heading(text="Skills", level=2),
                components.Table(
                    data=skills,
                    data_model=models.Skill,
                    columns=[
                        display.DisplayLookup(
                            field="skill_name",
                            table_width_percent=50,
                        ),
                        display.DisplayLookup(
                            field="level_of_confidence", table_width_percent=50
                        ),
                    ],
                ),
                components.Pagination(page=page, page_size=page_size, total=total),
            ]
        )
    ]
