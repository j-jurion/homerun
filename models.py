from sqlalchemy import Column, Integer, String, Double, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship

from database import Base
from utils.utils import get_official_and_personal_indices


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    date = Column(String, index=True, nullable=False)
    results = relationship("Result", back_populates="activity", cascade="all, delete-orphan")
    distance_tag = Column(String, index=True, nullable=False)

    environment = Column(String, index=True)
    training_type = Column(String, index=True)
    race_type = Column(String, index=True)
    with_friends = Column(Boolean, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month_id = Column(Integer, ForeignKey("monthly.id"), nullable=False)
    year_id = Column(Integer, ForeignKey("yearly.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    training_id = Column(Integer, ForeignKey("training.id"))

    user = relationship("User", back_populates="activities")
    monthly = relationship("Monthly", back_populates="activities")
    yearly = relationship("Yearly", back_populates="activities")
    event = relationship("Event", back_populates="activity")
    training = relationship("Training", back_populates="activities")


class Untraceable(Base):
    __tablename__ = "untraceables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    dates = Column(JSON, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="untraceables")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
    untraceables = relationship("Untraceable", back_populates="user", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    trainings = relationship("Training", back_populates="user", cascade="all, delete-orphan")
    monthly = relationship("Monthly", back_populates="user", cascade="all, delete-orphan")
    yearly = relationship("Yearly", back_populates="user", cascade="all, delete-orphan")


class Monthly(Base):
    __tablename__ = "monthly"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, index=True, nullable=False)

    activities = relationship("Activity", back_populates="monthly", cascade="all, delete-orphan")
    user = relationship("User", back_populates="monthly")

    @property
    def total_distance(self) -> int:
        total_distance = 0
        for activity in self.activities:
            official_index, personal_index = get_official_and_personal_indices(activity)
            if personal_index:
                total_distance += activity.results[personal_index].distance
            elif official_index:
                total_distance += activity.results[official_index].distance
            else:
                total_distance += activity.results[0].distance
        return total_distance

    @property
    def total_time(self) -> int:
        total_time = 0
        for activity in self.activities:
            official_index, personal_index = get_official_and_personal_indices(activity)
            if personal_index:
                total_time += activity.results[personal_index].time
            elif official_index:
                total_time += activity.results[official_index].time
            else:
                total_time += activity.results[0].time
        return total_time


class Yearly(Base):
    __tablename__ = "yearly"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, index=True, nullable=False)

    activities = relationship("Activity", back_populates="yearly", cascade="all, delete-orphan")
    user = relationship("User", back_populates="yearly")

    @property
    def total_distance(self) -> int:
        total_distance = 0
        for activity in self.activities:
            official_index, personal_index = get_official_and_personal_indices(activity)
            if personal_index:
                total_distance += activity.results[personal_index].distance
            elif official_index:
                total_distance += activity.results[official_index].distance
            else:
                total_distance += activity.results[0].distance
        return total_distance

    @property
    def total_time(self) -> int:
        total_time = 0
        for activity in self.activities:
            official_index, personal_index = get_official_and_personal_indices(activity)
            if personal_index:
                total_time += activity.results[personal_index].time
            elif official_index:
                total_time += activity.results[official_index].time
            else:
                total_time += activity.results[0].time
        return total_time


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    distance = Column(Double, index=True, nullable=False)
    distance_tag = Column(String)
    time = Column(Integer, index=True, nullable=False)
    pace = Column(Integer, index=True, nullable=False)
    speed = Column(Double, index=True, nullable=False)
    url = Column(String, index=True)
    tracking_type = Column(String)

    activity = relationship("Activity", back_populates="results")


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    time = Column(Integer, index=True)
    pace = Column(Integer, index=True)
    speed = Column(Double, index=True)

    event = relationship("Event", back_populates="goal")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    date = Column(String, index=True, nullable=False)
    environment = Column(String, index=True)
    race_type = Column(String, index=True)
    distance = Column(Double, index=True, nullable=False)
    distance_tag = Column(String, index=True, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    training_id = Column(Integer, ForeignKey("training.id"))

    goal = relationship("Goal", back_populates="event", cascade="all, delete-orphan", uselist=False)
    user = relationship("User", back_populates="events")
    activity = relationship("Activity", back_populates="event", uselist=False)
    training = relationship("Training", back_populates="events")


class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    begin_date = Column(String, index=True, nullable=False)
    end_date = Column(String, index=True, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    events = relationship("Event", back_populates="training")
    user = relationship("User", back_populates="trainings")
    activities = relationship("Activity", back_populates="training")
