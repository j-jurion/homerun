import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.pool import StaticPool

from database import Base, get_db
from main import app
from models import User, Training
from tests.utils import create_activity, create_training, get_training_json, create_event

TRAINING_URL = "/api/training"
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


def test_get_trainings(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    training_1 = create_training("training 1")
    training_2 = create_training("training 2")
    event_1 = create_event("event 1")
    event_1.training_id = 1
    event_2 = create_event("event 2")
    event_2.training_id = 2
    activity_1 = create_activity()
    activity_1.training_id = 1
    activity_2 = create_activity()
    activity_2.training_id = 2
    session.add(user_1)
    session.add(training_1)
    session.add(training_2)
    session.add(event_1)
    session.add(event_2)
    session.add(activity_1)
    session.add(activity_2)
    session.commit()

    response = client.get(TRAINING_URL + "/1/running")
    data = response.json()

    assert response.status_code == 200
    assert data[0] == get_training_json(1, "training 1", with_activity=True, with_events=True)
    assert data[1] == get_training_json(2, "training 2", with_activity=True, with_events=True)


def test_get_training(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    training_1 = create_training("training 1")
    training_2 = create_training("training 2")
    activity_1 = create_activity()
    activity_1.training_id = 1
    session.add(user)
    session.add(training_1)
    session.add(training_2)
    session.add(activity_1)
    session.commit()

    response = client.get(TRAINING_URL + "/1")
    data = response.json()

    assert response.status_code == 200
    assert data == get_training_json(1, "training 1")


def test_create_training(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    session.add(user)
    session.commit()

    response = client.post(
        TRAINING_URL + "/1",
        json=get_training_json(1, "training 1"),
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_training_json(1, "training 1", with_activity=False)
    assert len(user_data) == 1
    assert len(user_data[0].trainings) == 1
    assert user_data[0].trainings[0].name == "training 1"


def test_edit_training(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    training_1 = create_training("training 1")
    session.add(user)
    session.add(training_1)
    session.commit()

    response = client.put(
        TRAINING_URL + "/1",
        json=get_training_json(1, "training edited")
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_training_json(1, "training edited", with_activity=False)
    assert len(user_data) == 1
    assert len(user_data[0].trainings) == 1
    assert user_data[0].trainings[0].name == "training edited"


def test_remove_training(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    training_1 = create_training("training 1")
    training_2 = create_training("training 2")
    training_3 = create_training("training 3")
    session.add(user)
    session.add(training_1)
    session.add(training_2)
    session.add(training_3)
    session.commit()

    response = client.delete(TRAINING_URL + "/2")
    data = session.exec(select(Training)).all()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data[0].name == "training 1"
    assert data[1].name == "training 3"
    assert len(user_data) == 1
    assert len(user_data[0].trainings) == 2
    assert user_data[0].trainings[0].name == "training 1"
    assert user_data[0].trainings[1].name == "training 3"
