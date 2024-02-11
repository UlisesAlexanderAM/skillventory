import fastapi

from skillventory.database import config
from skillventory.routers import skills_v1
from skillventory.models import models

# dummy assignation to avoid deleting the unused import
# necessary for the correct creation of the db and tables
models_dummy = models

config.create_db_and_tables()

app = fastapi.FastAPI()
app.include_router(router=skills_v1.router)


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Welcome to Skillventory"}
