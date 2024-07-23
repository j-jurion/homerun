import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.pool import StaticPool
from sqlmodel import Session, SQLModel, select

from database import Base, get_db
from main import app
from models import User, Event
from tests.utils import create_activity, create_event, get_event_json

EVENTS_URL = "/api/events"
SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=session.get_bind())

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_get_events(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    event_1 = create_event("event 1")
    event_2 = create_event("event 2")
    activity_1 = create_activity()
    activity_1.event_id = 1
    activity_2 = create_activity()
    activity_2.event_id = 2
    session.add(user_1)
    session.add(event_1)
    session.add(event_2)
    session.add(activity_1)
    session.add(activity_2)
    session.commit()

    response = client.get(EVENTS_URL + "/1/running")
    data = response.json()

    assert response.status_code == 200
    assert data[0] == get_event_json(1, "event 1")
    assert data[1] == get_event_json(2, "event 2")


def test_get_event(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    event_1 = create_event("event 1")
    event_2 = create_event("event 2")
    activity_1 = create_activity()
    activity_1.event_id = 1
    session.add(user)
    session.add(event_1)
    session.add(event_2)
    session.add(activity_1)
    session.commit()

    response = client.get(EVENTS_URL + "/1")
    data = response.json()

    assert response.status_code == 200
    assert data == get_event_json(1, "event 1")


def test_create_event(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    session.add(user)
    session.commit()

    response = client.post(
        EVENTS_URL + "/1",
        json=get_event_json(1, "event 1"),
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_event_json(1, "event 1", with_activity=False)
    assert len(user_data) == 1
    assert len(user_data[0].events) == 1
    assert user_data[0].events[0].name == "event 1"


def test_edit_event(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    event_1 = create_event("event 1")
    session.add(user)
    session.add(event_1)
    session.commit()

    response = client.put(
        EVENTS_URL + "/1",
        json=get_event_json(1, "event edited")
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_event_json(1, "event edited", with_activity=False)
    assert len(user_data) == 1
    assert len(user_data[0].events) == 1
    assert user_data[0].events[0].name == "event edited"


def test_remove_activity(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    event_1 = create_event("event 1")
    event_2 = create_event("event 2")
    event_3 = create_event("event 3")
    session.add(user)
    session.add(event_1)
    session.add(event_2)
    session.add(event_3)
    session.commit()

    response = client.delete(EVENTS_URL + "/2")
    data = session.exec(select(Event)).all()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data[0].name == "event 1"
    assert data[1].name == "event 3"
    assert len(user_data) == 1
    assert len(user_data[0].events) == 2
    assert user_data[0].events[0].name == "event 1"
    assert user_data[0].events[1].name == "event 3"
