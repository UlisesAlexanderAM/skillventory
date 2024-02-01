import fastapi

from app.database import config
from app.routers import skills
from app.models import models

# dummy assignation to avoid deleting the unused import
# necessary for the correct creation of the db and tables
models_dummy = models

config.create_db_and_tables()

app = fastapi.FastAPI()
app.include_router(router=skills.router)


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Welcome to Skillventory"}
