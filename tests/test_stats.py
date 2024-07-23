import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel
from sqlmodel.pool import StaticPool

from database import Base, get_db
from main import app
from models import User
from tests.utils import get_stats_json, get_activity_json

STATS_URL = "/api/stats"
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


def test_get_stats(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    session.add(user_1)
    session.commit()

    response_activity_1 = client.post(
        ACTIVITY_URL + "/1",
        json=get_activity_json(1, "activity 1", "personal", "2023-11-22"),
    )
    response_activity_2 = client.post(
        ACTIVITY_URL + "/1",
        json=get_activity_json(1, "activity 2", "personal", "2023-11-23"),
    )
    response_activity_3 = client.post(
        ACTIVITY_URL + "/1",
        json=get_activity_json(1, "activity 3", "personal", "2023-12-22"),
    )
    response_activity_4 = client.post(
        ACTIVITY_URL + "/1",
        json=get_activity_json(1, "activity 4", "personal", "2024-11-22"),
    )
    response = client.get(STATS_URL + "/1/running")
    data = response.json()

    assert response.status_code == 200
    assert response_activity_1.status_code == 200
    assert response_activity_2.status_code == 200
    assert response_activity_3.status_code == 200
    assert response_activity_4.status_code == 200
    assert data == get_stats_json()

