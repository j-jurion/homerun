from enum import Enum
from datetime import date
from typing import Union, List

from pydantic import BaseModel, Field

from schemas.results import Result, ResultBase


class DistanceTagRunning(str, Enum):
    tag_5k_running = "5k"
    tag_10k_running = "10k"
    tag_15k_running = "15k"
    tag_21k_running = "half-marathon"
    tag_30k_running = "30k"
    tag_42k_running = "marathon"


class DistanceTagSwimming(str, Enum):
    tag_250_swimming = "250"
    tag_500_swimming = "500"
    tag_1000_swimming = "1000"
    tag_1500_swimming = "1500"
    tag_2000_swimming = "2000"


class ActivityType(str, Enum):
    running = "running"
    cycling = "cycling"
    swimming = "swimming"
    walking = "walking"
    duathlon = "duathlon"
    triathlon = "triathlon"
    other = "other"


class ActivityBase(BaseModel):
    name: str
    type: ActivityType
    description: Union[str, None] = Field(
        default=None, title="The description of the activity", max_length=300
    )
    date: date
    tags: Union[str, None] = Field(default=None, examples=["training", "race", "fun event", "training with company"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example run",
                    "type": "running",
                    "description": "This is an example",
                    "date": "2023-11-22",
                    "tags": "training",
                    "results": [
                        {
                            "distance": 10,
                            "time": 3000,
                            "tracking_type": "personal"
                        },
                        {
                            "distance": 10,
                            "time": 3000,
                            "tracking_type": "official"
                        }
                    ]
                }
            ]
        }
    }


class Activity(ActivityBase):
    id: int
    user_id: int
    month_id: int
    year_id: int
    distance_tag: DistanceTagRunning | DistanceTagSwimming | None = None
    results: List[Result]


class ActivityCreate(ActivityBase):
    results: List[ResultBase]
