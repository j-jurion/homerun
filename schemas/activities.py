from datetime import date
from typing import Union, List
from pydantic import BaseModel, Field

from definitions import ActivityType, Terrain, Pool, TrainingTypeSwimming, TrainingTypeRunning, RaceType
from schemas.results import Result, ResultBase


class ActivityBase(BaseModel):
    name: str
    type: ActivityType
    description: Union[str, None] = Field(
        default=None, title="The description of the activity", max_length=300
    )
    date: date

    environment: Terrain | Pool
    training_type: TrainingTypeRunning | TrainingTypeSwimming | None = None
    race_type: RaceType | None = None
    with_friends: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example run",
                    "type": "running",
                    "description": "This is an example",
                    "date": "2023-11-22",
                    "environment": "road",
                    "training_type": "base",
                    "with_friends": 0,
                    "results": [
                        {
                            "distance": 10,
                            "time": 3000,
                            "tracking_type": "personal"
                        },
                        {
                            "distance": 10,
                            "time": 3000,
                            "tracking_type": "official",
                            "url": ""
                        }
                    ],
                }
            ]
        }
    }


class Activity(ActivityBase):
    id: int
    user_id: int
    month_id: int
    year_id: int
    results: List[Result]
    distance_tag: str
    event_id: int | None = None
    training_id: int | None = None


class ActivityCreate(ActivityBase):
    results: List[ResultBase]
