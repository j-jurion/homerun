from enum import Enum
from typing import List, Union

from pydantic import BaseModel


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


class TrackingType(str, Enum):
    personal = "personal"
    official = "official"
    split = "split"


class ResultBase(BaseModel):
    tracking_type: TrackingType
    distance: float
    time: int


class Result(ResultBase):
    pace: int
    speed: float
    distance_tag: DistanceTagRunning | DistanceTagSwimming | None = None
