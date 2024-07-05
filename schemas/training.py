from datetime import date
from typing import Union, List
from pydantic import BaseModel, Field

from definitions import ActivityType
from schemas.activities import Activity
from schemas.events import Event


class TrainingBase(BaseModel):
    name: str
    begin_date: date
    end_date: date
    type: ActivityType
    description: Union[str, None] = Field(
        default=None, title="The description of the event", max_length=300
    )


class Training(TrainingBase):
    id: int
    user_id: int
    events: List[Event]
    activities: List[Activity]
