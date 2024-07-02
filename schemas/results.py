from enum import Enum
from typing import List, Union

from pydantic import BaseModel

from definitions import TrackingType, DistanceTagRunning, DistanceTagSwimming


class GoalBase(BaseModel):
    distance: float | None = None
    time: int | None = None


class Goal(GoalBase):
    pace: int | None = None
    speed: float | None = None


class ResultBase(BaseModel):
    distance: float
    time: int
    tracking_type: TrackingType
    url: str | None = None


class Result(ResultBase):
    pace: int
    speed: float
    distance_tag: DistanceTagRunning | DistanceTagSwimming | None = None
