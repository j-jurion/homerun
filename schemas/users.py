from typing import Union

from pydantic import BaseModel

from schemas.activities import Activity
from schemas.events import EventBase, Event
from schemas.training import Training
from schemas.untraceables import Untraceable


class UserBase(BaseModel):
    user_name: str


class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "New user",
                    "password": "T0p s3cret passw0rd"
                }
            ]
        }
    }


class User(UserBase):
    id: int
    activities: list[Activity] = []
    events: list[Event] = []
    trainings: list[Training] = []
    untraceables: list[Untraceable] = []


class UserUpdate(UserBase):
    user_name: Union[str, None] = None
    password: Union[str, None] = None
