from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas.untraceables import Untraceable, UntraceableCreate, UntraceableUpdate, UntraceableBase

router = APIRouter(
    prefix="/api/untraceables",
    tags=["untraceables"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=list[Untraceable])
def get_untraceables(user_id: int, db: Session = Depends(get_db)) -> List[Untraceable]:
    return crud.get_untraceables(db=db, user_id=user_id)


@router.get("/untraceable/{untraceable_id}", response_model=Untraceable)
def get_untraceable(untraceable_id: int, db: Session = Depends(get_db)) -> Untraceable:
    untraceable = crud.get_untraceable(db=db, untraceable_id=untraceable_id)
    if untraceable is None:
        raise HTTPException(status_code=404, detail="Untraceable activity not found")
    return untraceable


@router.post("/{user_id}", response_model=Untraceable)
def create_untraceable(
        user_id: int,
        untraceable: UntraceableCreate,
        db: Session = Depends(get_db),
):
    untraceable = crud.create_untraceable(db=db, untraceable=untraceable, user_id=user_id)
    print(untraceable.dates)
    return untraceable

@router.patch("/{untraceable_id}", response_model=Untraceable)
def edit_untraceable(untraceable_id: int, untraceable: UntraceableUpdate,
                  db: Session = Depends(get_db)) -> Untraceable:
    return crud.edit_untraceable(db=db, untraceable_id=untraceable_id, untraceable=untraceable)


@router.delete("/{untraceable_id}")
def remove_untraceable(untraceable_id: int, db: Session = Depends(get_db)):
    return crud.remove_untraceable(db=db, untraceable_id=untraceable_id)

@router.patch("/{untraceable_id}/new/{date}")
def add_date_untraceable(untraceable_id: int, new_date: str, db: Session = Depends(get_db)):
    return crud.add_date_untraceable(db=db, untraceable_id=untraceable_id, new_date=new_date)

@router.patch("/{untraceable_id}/remove/{date}")
def remove_date_untraceable(untraceable_id: int, remove_date: str, db: Session = Depends(get_db)):
    return crud.remove_date_untraceable(db=db, untraceable_id=untraceable_id, remove_date=remove_date)
