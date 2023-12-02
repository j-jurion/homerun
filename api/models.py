from sqlalchemy import Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(String, index=True, nullable=False)
    description = Column(String, index=True)
    date = Column(String, index=True, nullable=False)
    distance = Column(Double, index=True, nullable=False)
    distance_tag = Column(String)
    time = Column(Integer, index=True, nullable=False)
    pace = Column(Integer, index=True, nullable=False)
    speed = Column(Double, index=True, nullable=False)
    tags = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    month_id = Column(Integer, ForeignKey("monthly.id"), nullable=False)
    year_id = Column(Integer, ForeignKey("yearly.id"), nullable=False)

    user = relationship("User", back_populates="activities")
    monthly = relationship("Monthly", back_populates="activities")
    yearly = relationship("Yearly", back_populates="activities")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    activities = relationship("Activity", back_populates="user", cascade="all, delete-orphan")
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
            total_distance += activity.distance
        return total_distance

    @property
    def total_time(self) -> int:
        total_time = 0
        for activity in self.activities:
            total_time += activity.time
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
            total_distance += activity.distance
        return total_distance

    @property
    def total_time(self) -> int:
        total_time = 0
        for activity in self.activities:
            total_time += activity.time
        return total_time


