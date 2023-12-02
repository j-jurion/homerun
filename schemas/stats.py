from typing import List

from pydantic import BaseModel

from schemas.activities import Activity, ActivityType


class BestEffortsRunning(BaseModel):
    topThree5k: List[Activity]
    topThree10k: List[Activity]
    topThree15k: List[Activity]
    topThree21k: List[Activity]
    topThree30k: List[Activity]
    topThree45k: List[Activity]


class BestEffortsSwimming(BaseModel):
    topThree250: List[Activity]
    topThree500: List[Activity]
    topThree1000: List[Activity]
    topThree1500: List[Activity]
    topThree2000: List[Activity]


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
