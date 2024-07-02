from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from schemas.activities import Activity, ActivityCreate
from database import get_db
from schemas.events import EventBase, EventOutput

router = APIRouter(
    prefix="/api/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/{type}", response_model=list[EventBase])
def get_events(user_id: int, type: str, db: Session = Depends(get_db)) -> List[EventBase]:
    return crud.get_events(db=db, type=type, user_id=user_id)


@router.get("/{event_id}", response_model=EventBase)
def get_activity(event_id: int, db: Session = Depends(get_db)) -> EventBase:
    event = crud.get_event(db=db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{user_id}", response_model=EventOutput)
def create_event(
        user_id: int, event: EventBase, db: Session = Depends(get_db)
):
    return crud.create_event(db=db, event=event, user_id=user_id)

