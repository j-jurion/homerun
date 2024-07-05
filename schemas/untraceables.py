from datetime import date
from typing import Union, List
from pydantic import BaseModel, Field

from definitions import ActivityType, Terrain, Pool, TrainingTypeSwimming, TrainingTypeRunning, RaceType
from schemas.results import Result, ResultBase


class UntraceableBase(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the untraceable activity", max_length=300
    )


class UntraceableCreate(UntraceableBase):
    dates: List[date]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Frisbee training",
                    "description": "This is an example",
                    "dates": ["2023-11-22"],
                }
            ]
        }
    }


class Untraceable(UntraceableBase):
    id: int
    user_id: int
    dates: List[str]


class UntraceableUpdate(Untraceable):
    name:  Union[str, None] = None
    description:  Union[str, None] = None
    dates: Union[List[date], None] = None
