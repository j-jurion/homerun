from datetime import date
from typing import Union, List
from pydantic import BaseModel, Field

from definitions import ActivityType, Terrain, Pool, RaceType, DistanceTagRunning, DistanceTagSwimming
from schemas.activities import Activity
from schemas.results import Goal, GoalBase


class EventBase(BaseModel):
    name: str
    type: ActivityType
    description: Union[str, None] = Field(
        default=None, title="The description of the event", max_length=300
    )
    date: date

    environment: Terrain | Pool
    race_type: RaceType
    distance: float
    training_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "new event",
                    "type": "running",
                    "description": "new PR",
                    "date": "2024-07-03",
                    "environment": "road",
                    "race_type": "base",
                    "distance": 10,
                    "goal": {
                        "time": 1000
                    }
                }
            ]
        }
    }


class Event(EventBase):
    id: int
    user_id: int
    distance_tag: str
    goal: Goal | None = None
    activity: Activity | None = None


class EventCreate(EventBase):
    goal: GoalBase | None = None
