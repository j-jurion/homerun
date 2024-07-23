import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.pool import StaticPool

from main import app
from database import Base, get_db
from models import User
from tests.utils import get_user_json

USER_URL = "/api/users"
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


def test_get_users(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    user_2 = User(user_name="user 2", hashed_password="456789")
    session.add(user_1)
    session.add(user_2)
    session.commit()

    response = client.get(USER_URL + "/")
    data = response.json()

    assert response.status_code == 200
    assert data[0] == get_user_json(1, "user 1")
    assert data[1] == get_user_json(2, "user 2")


def test_get_user(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    user_2 = User(user_name="user 2", hashed_password="456789")
    session.add(user_1)
    session.add(user_2)
    session.commit()

    response = client.get(USER_URL + "/1")
    data = response.json()

    assert response.status_code == 200
    assert data == get_user_json(1, "user 1")


def test_create_user(client: TestClient):
    response = client.post(
        USER_URL + "/",
        json={"password": "654321",
              "user_name": "user a"
              },
    )
    data = response.json()

    assert response.status_code == 200
    assert data == get_user_json(1, "user a")


def test_edit_user(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    session.add(user_1)
    session.commit()

    response = client.patch(
        USER_URL + "/1",
        json={
            "password": "654321",
            "user_name": "user 3"
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "user_name": "user 3",
        "hashed_password": "654321notreallyhashed",
        "id": 1
    }


def test_remove_user(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    user_2 = User(user_name="user 2", hashed_password="123456")
    user_3 = User(user_name="user 3", hashed_password="123456")
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)
    session.commit()

    response = client.delete(USER_URL + "/2")
    data = session.exec(select(User)).all()

    assert response.status_code == 200
    assert data[0].user_name == "user 1"
    assert data[1].user_name == "user 3"
