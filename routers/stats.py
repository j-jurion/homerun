from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas.stats import Stats

router = APIRouter(
    prefix="/api/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}/{activity_type}", response_model=Stats)
def get_stats(user_id: int, activity_type: str, db: Session = Depends(get_db)) -> Stats:
    return crud.get_stats(db=db, user_id=user_id, activity_type=activity_type)


