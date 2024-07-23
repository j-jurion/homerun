import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Activity
from tests.utils import get_activity_json, create_activity

USER_URL = "/api/users"
ACTIVITY_URL = "/api/activities"
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


def test_read_activities(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    activity_1 = create_activity("activity 1")
    activity_2 = create_activity("activity 2")
    session.add(user)
    session.add(activity_1)
    session.add(activity_2)
    session.commit()

    response = client.get(ACTIVITY_URL + "/1/running")
    data = response.json()

    assert response.status_code == 200
    assert data[0] == get_activity_json(1, "activity 1")
    assert data[1] == get_activity_json(2, "activity 2")


def test_read_activity(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    activity_1 = create_activity("activity 1")
    activity_2 = create_activity("activity 2")
    session.add(user)
    session.add(activity_1)
    session.add(activity_2)
    session.commit()

    response = client.get(ACTIVITY_URL + "/1")
    data = response.json()

    assert response.status_code == 200
    assert data == get_activity_json(1, "activity 1")


def test_create_activity(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    session.add(user)
    session.commit()
    response = client.post(
        ACTIVITY_URL + "/1",
        json=get_activity_json(1, "activity 1"),
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_activity_json(1, "activity 1")
    assert len(user_data) == 1
    assert len(user_data[0].activities) == 1
    assert user_data[0].activities[0].name == "activity 1"


def test_edit_activity(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    activity_1 = create_activity("activity 1")
    session.add(user)
    session.add(activity_1)
    session.commit()

    response = client.put(
        ACTIVITY_URL + "/1",
        json=get_activity_json(1, "activity edited")
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_activity_json(1, "activity edited")
    assert len(user_data) == 1
    assert len(user_data[0].activities) == 1
    assert user_data[0].activities[0].name == "activity edited"


def test_remove_activity(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    activity_1 = create_activity("activity 1")
    activity_2 = create_activity("activity 2")
    activity_3 = create_activity("activity 3")
    session.add(user)
    session.add(activity_1)
    session.add(activity_2)
    session.add(activity_3)
    session.commit()

    response = client.delete(ACTIVITY_URL + "/2")
    data = session.exec(select(Activity)).all()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data[0].name == "activity 1"
    assert data[1].name == "activity 3"
    assert len(user_data) == 1
    assert len(user_data[0].activities) == 2
    assert user_data[0].activities[0].name == "activity 1"
    assert user_data[0].activities[1].name == "activity 3"
