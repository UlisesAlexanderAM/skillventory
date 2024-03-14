import fastapi
import fastui
from fastapi import responses

from skillventory.database import config
from skillventory.routers import skills_v1, skills_ui
from skillventory.models import models

# dummy assignation to avoid deleting the unused import
# necessary for the correct creation of the db and tables
models_dummy = models

config.create_db_and_tables()

app = fastapi.FastAPI()
app.include_router(router=skills_v1.router)
app.include_router(router=skills_ui.router)


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Welcome to Skillventory"}


@app.get("/{path:path}")
async def html_landing() -> responses.HTMLResponse:
    return responses.HTMLResponse(fastui.prebuilt_html(title="Skillventory"))
