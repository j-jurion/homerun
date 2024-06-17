from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from schemas.activities import Activity, ActivityCreate
from database import get_db

router = APIRouter(
    prefix="/api/activities",
    tags=["activities"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/{type}", response_model=list[Activity])
def get_activities(user_id: int, type: str, db: Session = Depends(get_db)) -> List[Activity]:
    return crud.get_activities(db=db, type=type, user_id=user_id)

@router.get("/{activity_id}", response_model=Activity)
def get_activity(activity_id: int, db: Session = Depends(get_db)) -> Activity:
    activity = crud.get_activity(db=db, activity_id=activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.post("/{user_id}", response_model=Activity)
def create_activity(
        user_id: int, activity: ActivityCreate, db: Session = Depends(get_db)
):
    return crud.create_activity(db=db, activity=activity, user_id=user_id)


@router.put("/{activity_id}")
def edit_activity(activity_id: int, activity: ActivityCreate,
                  db: Session = Depends(get_db)) -> Activity:
    return crud.edit_activity(db=db, activity_id=activity_id, activity=activity)


@router.delete("/{activity_id}")
def remove_activity(activity_id: int, db: Session = Depends(get_db)):
    return crud.remove_activity(db=db, activity_id=activity_id)
