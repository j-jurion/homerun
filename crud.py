import json
from typing import Any, Union
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
from definitions import ActivityType, DistanceTagRunning, DistanceTagSwimming
from schemas.activities import ActivityCreate
from schemas.events import EventBase, EventCreate
from schemas.results import ResultBase, Goal, GoalBase
from schemas.users import UserCreate, UserUpdate
from utils.utils import calculate_pace, calculate_speed, get_distance_tag, sort_on_pace, get_activity_distance_tag


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


def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()


def create_result(db: Session, result: ResultBase, activity_id: int,
                  activity_type: ActivityType):
    db_results = models.Result(
        **result.model_dump(),
        activity_id=activity_id,
        pace=calculate_pace(result.time, result.distance),
        speed=calculate_speed(result.time, result.distance),
        distance_tag=get_distance_tag(result.distance, activity_type),
    )
    db.add(db_results)
    db.commit()
    db.refresh(db_results)

    return db_results


def create_activity(db: Session, activity: ActivityCreate, user_id: int, event_id: int | None):
    db_activity = models.Activity(
        name=activity.name,
        type=activity.type,
        description=activity.description,
        date=activity.date,
        environment=activity.environment,
        training_type=activity.training_type,
        race_type=activity.race_type,
        with_friends=activity.with_friends,
        distance_tag=get_activity_distance_tag(activity.results, activity.type),
        user_id=user_id,
        month_id=get_month_id(db=db, date=activity.date, user_id=user_id, activity_type=activity.type.value),
        year_id=get_year_id(db=db, date=activity.date, user_id=user_id, activity_type=activity.type.value),
        event_id=event_id if event_id else None,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    for result in activity.results:
        create_result(db, result, db_activity.id, activity.type)

    return db_activity


def edit_activity(db: Session, activity_id: int, activity: ActivityCreate):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    remove_activity(db, activity_id)
    return create_activity(db, activity, db_activity.user_id)


def remove_activity(db: Session, activity_id: int):
    db_activity = db.get(models.Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(db_activity)
    db.commit()

    return {"ok": True}


def get_month_id(db: Session, date: date, user_id: int, activity_type: str, create_if_none=True) -> int:
    month = f"{date.year}-{date.month}"
    db_monthly = db.query(models.Monthly).filter(models.Monthly.month == month,
                                                 models.Monthly.activity_type == activity_type).first()
    if create_if_none and not db_monthly:
        return create_monthly(db=db, month=month, user_id=user_id, activity_type=activity_type).id
    else:
        return db_monthly.id


def get_year_id(db: Session, date: date, user_id: int, activity_type: str, create_if_none=True) -> Union[int, None]:
    year = str(date.year)
    db_yearly = db.query(models.Yearly).filter(models.Yearly.year == year,
                                               models.Yearly.activity_type == activity_type).first()
    if create_if_none and not db_yearly:
        return create_yearly(db=db, year=year, user_id=user_id, activity_type=activity_type).id
    else:
        return db_yearly.id


def create_monthly(db: Session, month: str, user_id: int, activity_type: str):
    db_monthly = db.query(models.Monthly).filter(
        models.Monthly.month == month, models.Monthly.activity_type == activity_type).first()
    if not db_monthly:
        db_monthly = models.Monthly(month=month, user_id=user_id, activity_type=activity_type)
        db.add(db_monthly)
        db.commit()
    return db_monthly


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
    if activity_type == ActivityType.running:
        for tag in DistanceTagRunning:
            best_efforts[tag.value] = db.query(models.Activity).join(models.Result) \
                .filter(models.Activity.user_id == user_id, models.Activity.type == activity_type,
                        models.Activity.distance_tag == tag).all()

    elif activity_type == ActivityType.swimming:
        for tag in DistanceTagSwimming:
            best_efforts[tag.value] = db.query(models.Activity).join(models.Result) \
                .filter(models.Activity.user_id == user_id, models.Activity.type == activity_type,
                        models.Activity.distance_tag == tag).all()
    else:
        return {}

    for key in best_efforts.keys():
        best_efforts_by_distance = best_efforts[key].sort(key=sort_on_pace)
        if best_efforts_by_distance:
            best_efforts[key] = best_efforts_by_distance[:3]

    return best_efforts


def get_events(db: Session, type: str, user_id: int):
    return db.query(models.Event).filter(models.Event.user_id == user_id).filter(
        models.Event.type == type).all()


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def create_goal(db: Session, goal: GoalBase, distance: float, event_id: int):
    db_goal = models.Goal(
        **goal.model_dump(),
        event_id=event_id,
        pace=calculate_pace(goal.time, distance),
        speed=calculate_speed(goal.time, distance),
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    print(db_goal)

    return db_goal


def create_event(db: Session, event: EventCreate, user_id: int):
    db_event = models.Event(
        name=event.name,
        type=event.type,
        description=event.description,
        date=event.date,
        distance=event.distance,
        environment=event.environment,
        race_type=event.race_type,
        distance_tag=get_distance_tag(event.distance, event.type),
        user_id=user_id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    if event.goal:
        create_goal(db, event.goal, event.distance, db_event.id)

    return db_event


def remove_event(db: Session, event_id: int):
    db_event = db.get(models.Event, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()

    return {"ok": True}


def edit_event(db: Session, event_id: int, event: EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    remove_event(db, event_id)
    return create_event(db, event, db_event.user_id)
