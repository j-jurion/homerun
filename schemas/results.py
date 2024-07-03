from pydantic import BaseModel

from definitions import TrackingType, DistanceTagRunning, DistanceTagSwimming


class GoalBase(BaseModel):
    time: int


class Goal(GoalBase):
    pace: int
    speed: float


class ResultBase(BaseModel):
    distance: float
    time: int
    tracking_type: TrackingType
    url: str | None = None


class Result(ResultBase):
    pace: int
    speed: float
    distance_tag: DistanceTagRunning | DistanceTagSwimming | None = None
