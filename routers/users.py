from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from schemas.users import User, UserCreate, UserUpdate
from database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_user_name(db, user_name=user.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User name already registered")
    return crud.create_user(db=db, user=user)


@router.patch("/{user_id}")
def edit_user(user_id: int, user: UserUpdate,
              db: Session = Depends(get_db)):
    return crud.edit_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return crud.remove_user(db=db, user_id=user_id)
