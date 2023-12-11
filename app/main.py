import fastapi

from app.database import config
from app.routers import skills

config.create_db_and_tables()

app = fastapi.FastAPI()
app.include_router(router=skills.router)
