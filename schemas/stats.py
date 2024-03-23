from typing import List

from pydantic import BaseModel

from schemas.activities import Activity, ActivityType


class Grouped(BaseModel):
    activity_type: ActivityType
    activities: List[Activity]
    total_distance: float
    total_time: int


class Monthly(Grouped):
    month: str


class Yearly(Grouped):
    year: str


class Stats(BaseModel):
    monthly: List[Monthly]
    yearly: List[Yearly]
    best_efforts: dict[str, List[Activity]]
