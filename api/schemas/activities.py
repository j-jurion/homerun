from enum import Enum
from datetime import date
from typing import List

from pydantic import BaseModel, Field


class ActivityType(str, Enum):
    running = "running"
    cycling = "cycling"
    swimming = "swimming"
    walking = "walking"
    triathlon = "triathlon"


class DistanceTag(str, Enum):
    tag_5k_running = "5k"
    tag_10k_running = "10k"
    tag_15k_running = "15k"
    tag_21k_running = "half-marathon"
    tag_30k_running = "30k"
    tag_42k_running = "marathon"

    tag_250_swimming = "250"
    tag_500_swimming = "500"
    tag_1000_swimming = "1000"
    tag_1500_swimming = "1500"
    tag_2000_swimming = "2000"


class ActivityBase(BaseModel):
    name: str
    type: ActivityType
    description: str | None = Field(
        default=None, title="The description of the activity", max_length=300
    )
    date: date
    distance: float
    time: int
    tags: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example run",
                    "type": "running",
                    "description": "This is an example",
                    "date": "2023-11-22",
                    "distance": 10,
                    "time": 3000,
                    "tags": "race"
                }
            ]
        }
    }


class Activity(ActivityBase):
    id: int
    user_id: int
    month_id: int
    year_id: int
    pace: int
    speed: float
    distance_tag: DistanceTag | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    name: str | None = None
    type: ActivityType | None = None
    description: str | None = Field(
        default=None, title="The description of the activity", max_length=300
    )
    date: date | None = date
    distance: float | None = None
    time: int | None = None
