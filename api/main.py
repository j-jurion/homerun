from fastapi import FastAPI
from starlette.responses import FileResponse

import models
from database import engine
from routers import users, activities, stats

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Homerun", redoc_url=None)

app.include_router(users.router)
app.include_router(activities.router)
app.include_router(stats.router)

favicon_path = 'static/logo.ico'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

