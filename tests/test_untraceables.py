import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select
from sqlmodel.pool import StaticPool

from main import app
from database import Base, get_db
from models import User, Untraceable
from tests.utils import create_untraceable, get_untraceable_json, get_untraceables_json

UNTRACEABLES_URL = "/api/untraceables"
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


def test_get_untraceables(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    untraceable_2 = create_untraceable("untraceable 2")
    session.add(user_1)
    session.add(untraceable_1)
    session.add(untraceable_2)
    session.commit()

    response = client.get(UNTRACEABLES_URL + "/1")
    data = response.json()

    assert response.status_code == 200
    assert data == get_untraceables_json(["untraceable 1", "untraceable 2"])


def test_get_untraceable(session: Session, client: TestClient):
    user_1 = User(user_name="user 1", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    untraceable_2 = create_untraceable("untraceable 2")
    session.add(user_1)
    session.add(untraceable_1)
    session.add(untraceable_2)
    session.commit()

    response = client.get(UNTRACEABLES_URL + "/untraceable/2")
    data = response.json()

    assert response.status_code == 200
    assert data == get_untraceable_json(2, "untraceable 2")


def test_create_untraceable(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    session.add(user)
    session.commit()
    response = client.post(
        UNTRACEABLES_URL + "/1",
        json=get_untraceable_json(1, "untraceable 1"),
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_untraceable_json(1, "untraceable 1")
    assert len(user_data) == 1
    assert len(user_data[0].untraceables) == 1
    assert user_data[0].untraceables[0].name == "untraceable 1"


def test_edit_untraceable(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    untraceable_1 = create_untraceable()
    session.add(user)
    session.add(untraceable_1)
    session.commit()

    response = client.patch(
        UNTRACEABLES_URL + "/1",
        json={
            'dates': [
                '2023-11-22',
                '2023-11-23',
                '2024-11-22'
            ],
            'name': "untraceable edited",
        }
    )
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_untraceable_json(
        1,
        "untraceable edited",
        [
            '2023-11-22',
            '2023-11-23',
            '2024-11-22'
        ])
    assert len(user_data) == 1
    assert len(user_data[0].untraceables) == 1
    assert user_data[0].untraceables[0].name == "untraceable edited"


def test_remove_untraceable(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    untraceable_2 = create_untraceable("untraceable 2")
    untraceable_3 = create_untraceable("untraceable 3")
    session.add(user)
    session.add(untraceable_1)
    session.add(untraceable_2)
    session.add(untraceable_3)
    session.commit()

    response = client.delete(UNTRACEABLES_URL + "/2")
    data = session.exec(select(Untraceable)).all()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data[0].name == "untraceable 1"
    assert data[1].name == "untraceable 3"
    assert len(user_data) == 1
    assert len(user_data[0].untraceables) == 2
    assert user_data[0].untraceables[0].name == "untraceable 1"
    assert user_data[0].untraceables[1].name == "untraceable 3"


def test_add_date_untraceable(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    session.add(user)
    session.add(untraceable_1)
    session.commit()

    response = client.patch(UNTRACEABLES_URL + "/new/1/2024-11-22")
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_untraceable_json(
        1,
        "untraceable 1",
        [
            '2023-11-22',
            '2023-11-23',
            '2024-11-22'
        ])
    assert len(user_data) == 1
    assert len(user_data[0].untraceables) == 1
    assert user_data[0].untraceables[0].name == "untraceable 1"
    assert user_data[0].untraceables[0].dates == [
        '2023-11-22',
        '2023-11-23',
        '2024-11-22'
    ]


def test_add_date_untraceable_already_assigned(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    session.add(user)
    session.add(untraceable_1)
    session.commit()

    response = client.patch(UNTRACEABLES_URL + "/new/1/2023-11-22")

    assert response.status_code == 400


def test_remove_date_untraceable(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    session.add(user)
    session.add(untraceable_1)
    session.commit()

    response = client.patch(UNTRACEABLES_URL + "/remove/1/2023-11-23")
    data = response.json()
    user_data = session.exec(select(User).filter(User.id == 1)).all()

    assert response.status_code == 200
    assert data == get_untraceable_json(
        1,
        "untraceable 1",
        [
            '2023-11-22',
        ])
    assert len(user_data) == 1
    assert len(user_data[0].untraceables) == 1
    assert user_data[0].untraceables[0].name == "untraceable 1"
    assert user_data[0].untraceables[0].dates == [
        '2023-11-22',
    ]


def test_remove_date_untraceable_date_not_assigned(session: Session, client: TestClient):
    user = User(user_name="user", hashed_password="123456")
    untraceable_1 = create_untraceable("untraceable 1")
    session.add(user)
    session.add(untraceable_1)
    session.commit()

    response = client.patch(UNTRACEABLES_URL + "/remove/1/2024-11-23")

    assert response.status_code == 400
