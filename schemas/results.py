from enum import Enum
from typing import List, Union

from pydantic import BaseModel

from definitions import TrackingType, DistanceTagRunning, DistanceTagSwimming


class ResultBase(BaseModel):
    tracking_type: TrackingType
    distance: float
    time: int
    url: str | None = None


class Result(ResultBase):
    pace: int
    speed: float
    distance_tag: DistanceTagRunning | DistanceTagSwimming | None = None
