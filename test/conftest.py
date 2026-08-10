from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from enums.stock_movement_type import StockMovementType
from main import app, limiter
from models.stock_movement import StockMovement
from models.user import User
from security import hash_password

limiter.enabled = False

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_email_task():
    with patch("services.auth.send_verification_email_task.delay") as mock:
        yield mock


@pytest.fixture
def auth_headers(client, db_session):
    user = User(
        username="testuser",
        email="testuser@test.com",
        password=hash_password("testuser"),
        role="user",
    )

    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "testuser", "password": "testuser"}
    )

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(client, db_session):
    admin = User(
        username="admin_test",
        email="admin_test@test.com",
        password=hash_password("admin_test"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "admin_test", "password": "admin_test"}
    )

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user(db_session):
    user = User(
        username="otheruser",
        email="other@test.com",
        password=hash_password("otheruser"),
        role="user",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def current_user(db_session):
    return db_session.query(User).filter(User.username == "testuser").first()


@pytest.fixture
def stock_movement(db_session):
    movement = StockMovement(
        product_id=1,
        user_id=1,
        quantity=10,
        type=StockMovementType.IN,
    )

    db_session.add(movement)
    db_session.commit()
    db_session.refresh(movement)

    return movement


@pytest.fixture
def admin_user(db_session):
    admin = User(
        username="admin_service_test",
        email="admin_service_test@test.com",
        password=hash_password("admin_service_test"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    return admin
