from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

import models
from schemas.activities import ActivityCreate, ActivityUpdate, ActivityType, DistanceTag
from schemas.users import UserCreate, UserUpdate


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_user_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(user_name=user.user_name, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def edit_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def remove_user(db: Session, user_id: int):
    db_user = db.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}


def get_activities(db: Session, type: str, user_id: int):
    return db.query(models.Activity).filter(models.Activity.user_id == user_id).filter(
        models.Activity.type == type).all()


def create_activity(db: Session, activity: ActivityCreate, user_id: int):
    db_activity = models.Activity(
        **activity.model_dump(),
        user_id=user_id,
        month_id=get_month_id(db=db, date=activity.date, user_id=user_id, activity_type=activity.type.value),
        year_id=get_year_id(db=db, date=activity.date, user_id=user_id, activity_type=activity.type.value),
        pace=calculate_pace(activity.time, activity.distance),
        speed=calculate_speed(activity.time, activity.distance),
        distance_tag=get_distance_tag(activity.distance, activity.type)
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


def edit_activity(db: Session, activity_id: int, activity: ActivityUpdate):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity_data = activity.model_dump(exclude_unset=True)
    for key, value in activity_data.items():
        setattr(db_activity, key, value)
    db_activity.pace = calculate_pace(db_activity.time, db_activity.distance)
    db_activity.speed = calculate_speed(db_activity.time, db_activity.distance)
    db_activity.distance_tag = get_distance_tag(db_activity.distance, db_activity.type)

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


def remove_activity(db: Session, activity_id: int):
    db_activity = db.get(models.Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(db_activity)
    db.commit()

    return {"ok": True}


def calculate_pace(time: int, distance: float) -> int:
    return round(time / distance)


def calculate_speed(time: int, distance: float):
    return distance * 3600 / time


def get_distance_tag(distance: float, type: ActivityType):
    if type is ActivityType.running:
        if get_margin(5.0)[0] <= distance <= get_margin(5.0)[1]:
            return DistanceTag.tag_5k_running
        if get_margin(10.0)[0] <= distance <= get_margin(10.0)[1]:
            return DistanceTag.tag_10k_running
        if get_margin(15.0)[0] <= distance <= get_margin(15.0)[1]:
            return DistanceTag.tag_15k_running
        if get_margin(21.1)[0] <= distance <= get_margin(21.1)[1]:
            return DistanceTag.tag_21k_running
        if get_margin(30.0)[0] <= distance <= get_margin(30.0)[1]:
            return DistanceTag.tag_30k_running
        if get_margin(42.2)[0] <= distance <= get_margin(42.2)[1]:
            return DistanceTag.tag_42k_running
    elif type is ActivityType.swimming:
        if get_margin(0.250)[0] <= distance <= get_margin(0.250)[1]:
            return DistanceTag.tag_250_swimming
        if get_margin(0.500)[0] <= distance <= get_margin(0.500)[1]:
            return DistanceTag.tag_500_swimming
        if get_margin(1.0)[0] <= distance <= get_margin(1.0)[1]:
            return DistanceTag.tag_1000_swimming
        if get_margin(1.5)[0] <= distance <= get_margin(1.5)[1]:
            return DistanceTag.tag_1500_swimming
        if get_margin(2.0)[0] <= distance <= get_margin(2.0)[1]:
            return DistanceTag.tag_2000_swimming


def get_margin(number: float):
    return [number - number / 25, number + number / 25]


def get_month_id(db: Session, date: date, user_id: int, activity_type: str, create_if_none=True) -> int:
    month = f"{date.year}-{date.month}"
    db_monthly = db.query(models.Monthly).filter(models.Monthly.month == month,
                                                 models.Monthly.activity_type == activity_type).first()
    if create_if_none and not db_monthly:
        return create_monthly(db=db, month=month, user_id=user_id, activity_type=activity_type).id
    else:
        return db_monthly.id


def create_monthly(db: Session, month: str, user_id: int, activity_type: str):
    db_monthly = db.query(models.Monthly).filter(
        models.Monthly.month == month, models.Monthly.activity_type == activity_type).first()
    if not db_monthly:
        db_monthly = models.Monthly(month=month, user_id=user_id, activity_type=activity_type)
        db.add(db_monthly)
        db.commit()
    return db_monthly


def get_year_id(db: Session, date: date, user_id: int, activity_type: str, create_if_none=True) -> int | None:
    year = str(date.year)
    db_yearly = db.query(models.Yearly).filter(models.Yearly.year == year,
                                               models.Yearly.activity_type == activity_type).first()
    if create_if_none and not db_yearly:
        return create_yearly(db=db, year=year, user_id=user_id, activity_type=activity_type).id
    else:
        return db_yearly.id


def create_yearly(db: Session, year: str, user_id: int, activity_type: str):
    db_yearly = db.query(models.Yearly).filter(
        models.Yearly.year == year, models.Yearly.activity_type == activity_type).first()
    if not db_yearly:
        db_yearly = models.Yearly(year=year, user_id=user_id, activity_type=activity_type)
        db.add(db_yearly)
        db.commit()
    return db_yearly


def get_stats(db: Session, user_id: int, activity_type: str):
    monthlies = db.query(models.Monthly) \
        .filter(models.Monthly.user_id == user_id, models.Monthly.activity_type == activity_type)
    yearlies = db.query(models.Yearly) \
        .filter(models.Yearly.user_id == user_id, models.Yearly.activity_type == activity_type)

    return {'monthly': monthlies, 'yearly': yearlies,
            'best_efforts': get_best_efforts(db=db, user_id=user_id, activity_type=activity_type)}


def get_best_efforts(db: Session, user_id: int, activity_type: str):
    best_efforts = {}
    for tag in DistanceTag:
        best_efforts[tag.value] = db.query(models.Activity) \
            .filter(models.Activity.user_id == user_id, models.Activity.type == activity_type,
                    models.Activity.distance_tag == tag) \
            .order_by(models.Activity.pace).limit(3).all()
    return best_efforts
