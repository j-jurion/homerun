import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.responses import FileResponse

import models
from database import engine
from routers import users, activities, stats, config, events
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Homerun",
    redoc_url=None,
)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(activities.router)
app.include_router(events.router)
app.include_router(stats.router)
app.include_router(config.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
