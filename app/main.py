import fastapi

from app.database import config
from app.routers import skills

config.Base.metadata.create_all(bind=config.engine)

app = fastapi.FastAPI()
app.include_router(router=skills.router)
