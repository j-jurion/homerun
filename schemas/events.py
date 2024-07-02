from datetime import date
from typing import Union, List
from pydantic import BaseModel, Field

from definitions import ActivityType, Terrain, Pool, RaceType, DistanceTagRunning, DistanceTagSwimming
from schemas.activities import Activity
from schemas.results import Goal, GoalBase


class EventBase(BaseModel):
    name: str
    user_id: int
    type: ActivityType
    description: Union[str, None] = Field(
        default=None, title="The description of the event", max_length=300
    )
    date: date

    environment: Terrain | Pool
    race_type: RaceType
    goal: GoalBase | None = None

    # model_config = {
    #        "json_schema_extra": {
    #            "examples": [
    #                {
    #
    #                }
    #            ]
    #        }
    #    }


class EventOutput(EventBase):
    distance_tag: str
    goal: Goal | None = None
