from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from schemas.activities import Activity, ActivityCreate
from database import get_db
from schemas.events import Event, EventCreate
from schemas.training import Training, TrainingBase

router = APIRouter(
    prefix="/api/training",
    tags=["training"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/{type}", response_model=list[Training])
def get_trainings(user_id: int, type: str, db: Session = Depends(get_db)) -> List[Training]:
    return crud.get_trainings(db=db, type=type, user_id=user_id)


@router.get("/{training_id}", response_model=Training)
def get_training(training_id: int, db: Session = Depends(get_db)) -> Training:
    training = crud.get_training(db=db, training_id=training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Training not found")
    return training


@router.post("/{user_id}", response_model=Training)
def create_training(
        user_id: int, training: TrainingBase, db: Session = Depends(get_db)
):
    return crud.create_training(db=db, training=training, user_id=user_id)

@router.put("/{training_id}")
def edit_training(training_id: int, training: TrainingBase,
               db: Session = Depends(get_db)) -> Training:
    return crud.edit_training(db=db, training_id=training_id, training=training)


@router.delete("/{training_id}")
def remove_training(training_id: int, db: Session = Depends(get_db)):
    return crud.remove_training(db=db, training_id=training_id)
