from models.user import User
from security import hash_password


def test_login_success(client, db_session):
    user = User(
        username="test",
        email="test@test.com",
        password=hash_password("test123")
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "test",
            "password": "test123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_username(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "test1",
            "password": "test1"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_login_invalid_password(client, db_session):
    user = User(
        username="testwrong",
        email="testwrong@test.com",
        password=hash_password("wrongpassword")
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={
            "username": "testwrong",
            "password": "wrongpassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"

def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "irhad",
            "email": "irhad@test.com",
            "password": "irhad123"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully."

def test_register_existing_email(client, db_session):
    user = User(
        username="testexisting",
        email="testexisting@test.com",
        password=hash_password("testexisting")
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/register",
        json={
            "username": "testexisting",
            "email": "testexisting@test.com",
            "password": "testexisting"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."