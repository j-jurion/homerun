from typing import Union

from pydantic import BaseModel

from schemas.activities import Activity


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


class UserUpdate(UserBase):
    user_name: Union[str, None] = None
    password: Union[str, None] = None
