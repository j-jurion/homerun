from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from definitions import DistanceTagRunning, ActivityType, RaceType, TrainingTypeSwimming, TrainingTypeRunning, Pool, \
    Terrain, TrackingType
from schemas.activities import Activity, ActivityCreate
from database import get_db

router = APIRouter(
    prefix="/api/config",
    tags=["config"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=dict[str, list[Any]])
def get_config() -> dict[str, list[Any]]:
    return {
        "activity_type": [e.value for e in ActivityType],
        "tracking": [e.value for e in TrackingType],
        "terrain": [e.value for e in Terrain],
        "pool": [e.value for e in Pool],
        "training_type_running": [e.value for e in TrainingTypeRunning],
        "training_type_swimming": [e.value for e in TrainingTypeSwimming],
        "race_type": [e.value for e in RaceType],
    }



