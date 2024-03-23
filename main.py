import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.responses import FileResponse

import models
from database import engine
from routers import users, activities, stats
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Homerun",
    redoc_url=None,
)

app.include_router(users.router)
app.include_router(activities.router)
app.include_router(stats.router)

favicon_path = 'static/logo.ico'


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
