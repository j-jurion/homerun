from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from schemas.activities import Activity, ActivityCreate
from database import get_db
from schemas.events import Event, EventCreate

router = APIRouter(
    prefix="/api/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/{type}", response_model=list[Event])
def get_events(user_id: int, type: str, db: Session = Depends(get_db)) -> List[Event]:
    return crud.get_events(db=db, type=type, user_id=user_id)


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    event = crud.get_event(db=db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{user_id}", response_model=Event)
def create_event(
        user_id: int, event: EventCreate, db: Session = Depends(get_db)
):
    event = crud.create_event(db=db, event=event, user_id=user_id)
    event.activity = None
    return event


@router.put("/{event_id}")
def edit_event(event_id: int, event: EventCreate,
               db: Session = Depends(get_db)) -> Event:
    return crud.edit_event(db=db, event_id=event_id, event=event)


@router.delete("/{event_id}")
def remove_event(event_id: int, db: Session = Depends(get_db)):
    return crud.remove_event(db=db, event_id=event_id)
