import pytest

from core.exception import BadRequestException, NotFoundException
from models.product import Item
from models.user import User
from schemas.user import UserCreate
from services.user import UserService


@pytest.mark.asyncio
async def test_get_users(client, admin_auth_headers, db_session):
    user1 = User(
        username="TestUser", email="testuser@test.com", password="testuser", role="user"
    )
    user2 = User(
        username="TestUser2",
        email="testuser2@test.com",
        password="testuser2",
        role="user",
    )
    user3 = User(
        username="TestUser3",
        email="testuser3@test.com",
        password="testuser3",
        role="user",
    )

    db_session.add_all([user1, user2, user3])
    db_session.commit()

    response = client.get("/users", headers=admin_auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert len(data["users"]) >= 3

    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] == 4
    assert data["total_pages"] == 1

    usernames = [user["username"] for user in data["users"]]

    assert "TestUser" in usernames
    assert "TestUser2" in usernames
    assert "TestUser3" in usernames

    assert data["users"][0]["is_verified"] is False


def test_get_users_pagination(client, admin_auth_headers, db_session):
    for i in range(13):
        user = User(
            username=f"User {i + 1}",
            email=f"testuser{i + 1}@test.com",
            password=f"testuser{i + 1}",
            role="user",
        )
        db_session.add(user)

    db_session.commit()

    response = client.get(
        "/users/?page=2&limit=10",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 10
    assert data["total"] >= 13
    assert data["total_pages"] == (data["total"] + data["limit"] - 1) // data["limit"]
    assert len(data["users"]) == data["total"] - 10


@pytest.mark.asyncio
async def test_get_users_from_cache(monkeypatch, db_session, current_user):
    cached_movements = {
        "users": [
            {
                "id": 1,
                "username": "TestUser4",
                "email": "testuser4@test.com",
                "role": "user",
                "is_verified": False,
            }
        ],
        "page": 1,
        "limit": 10,
        "total": 1,
        "total_pages": 1,
    }

    async def mock_get_cache(key):
        return cached_movements

    # ovdje koristim kao funkciju da privremeno promijenim ponasanje neke funkcije koju testiram
    # u stvari laziram Redis
    monkeypatch.setattr(
        "services.user.get_cache",
        mock_get_cache,
    )

    def mock_get_all(db):
        pytest.fail("Repository should not be called when cache exists")

    monkeypatch.setattr(
        "services.user.user_repository.get_all",
        mock_get_all,
    )

    result = await UserService.get_users(db_session, current_user, 1, 10)

    assert len(result["users"]) == 1
    assert result["users"][0].username == "TestUser4"
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["total"] == 1
    assert result["total_pages"] == 1


@pytest.mark.asyncio
async def test_get_users_cache_miss(monkeypatch, db_session, current_user):
    user = User(
        id=1,
        username="usertest",
        password="usertest",
        email="otheruser@test.com",
        role="user",
        is_verified=False,
    )

    async def mock_get_cache(key):
        return None

    cache_data = {}

    async def mock_set_cache(key, value, expire):
        cache_data["key"] = key
        cache_data["value"] = value
        cache_data["expire"] = expire

    monkeypatch.setattr(
        "services.user.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr("services.user.set_cache", mock_set_cache)

    def mock_get_all(db, page, limit):
        return [user], 1

    monkeypatch.setattr("services.user.user_repository.get_all", mock_get_all)

    result = await UserService.get_users(db_session, current_user, 1, 10)

    assert len(result) == 5
    assert result["users"][0].username == "usertest"
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["total"] == 1
    assert result["total_pages"] == 1

    assert cache_data["key"] == "users:list:1:10"
    assert cache_data["expire"] == 300


@pytest.mark.asyncio
async def test_get_users_empty(monkeypatch, db_session, current_user):
    async def mock_get_cache(key):
        return None

    def mock_get_all(db, page, limit):
        return [], 0

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr("services.user.get_cache", mock_get_cache)

    monkeypatch.setattr("services.user.set_cache", mock_set_cache)

    monkeypatch.setattr(
        "services.user.user_repository.get_all",
        mock_get_all,
    )

    result = await UserService.get_users(db_session, current_user, 1, 10)

    assert result["users"] == []
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["total"] == 0
    assert result["total_pages"] == 0


@pytest.mark.asyncio
async def test_create_user_success(monkeypatch, db_session, other_user):
    user = UserCreate(
        username="newuser",
        email="newuser@test.com",
        password="password123",
    )

    async def mock_delete_cache_pattern(pattern):
        pass

    monkeypatch.setattr(
        "services.user.delete_cache_pattern",
        mock_delete_cache_pattern,
    )

    def mock_get_by_username(db, username):
        return None

    def mock_get_by_email(db, email):
        return None

    def mock_create(db, new_user):
        new_user.id = 10
        return new_user

    monkeypatch.setattr(
        "services.user.user_repository.get_by_username",
        mock_get_by_username,
    )

    monkeypatch.setattr(
        "services.user.user_repository.get_by_email",
        mock_get_by_email,
    )

    monkeypatch.setattr(
        "services.user.user_repository.create",
        mock_create,
    )

    result = await UserService.create_user(
        user,
        db_session,
        other_user,
    )

    assert result.id == 10
    assert result.username == "newuser"
    assert result.email == "newuser@test.com"


@pytest.mark.asyncio
async def test_create_user_username_exists(monkeypatch, db_session, current_user):
    user = UserCreate(
        username="existinguser",
        email="newuser@test.com",
        password="password123",
    )

    existing_user = User(
        username="existinguser",
        email="existing@test.com",
        password="hashed",
    )

    def mock_get_by_username(db, username):
        return existing_user

    monkeypatch.setattr(
        "services.user.user_repository.get_by_username",
        mock_get_by_username,
    )

    with pytest.raises(BadRequestException) as exc:
        await UserService.create_user(
            user,
            db_session,
            current_user,
        )

    assert str(exc.value) == "Username already exists"


@pytest.mark.asyncio
async def test_create_user_email_exists(monkeypatch, db_session, current_user):
    user = UserCreate(
        username="newuser",
        email="existing@test.com",
        password="password123",
    )

    existing_user = User(
        username="existinguser",
        email="existing@test.com",
        password="hashed",
    )

    def mock_get_by_username(db, username):
        return None

    def mock_get_by_email(db, email):
        return existing_user

    monkeypatch.setattr(
        "services.user.user_repository.get_by_username",
        mock_get_by_username,
    )

    monkeypatch.setattr(
        "services.user.user_repository.get_by_email",
        mock_get_by_email,
    )

    with pytest.raises(BadRequestException) as exc:
        await UserService.create_user(
            user,
            db_session,
            current_user,
        )

    assert str(exc.value) == "Email already exists"


@pytest.mark.asyncio
async def test_delete_user_success(monkeypatch, db_session, other_user):
    user = User(
        id=5,
        username="deleteuser",
        email="delete@test.com",
        password="hashed",
        role="user",
    )

    cache_data = {}

    def mock_get_by_id(db, user_id):
        return user

    def mock_delete(db, user):
        cache_data["deleted_user"] = user

    async def mock_delete_cache_pattern(pattern):
        cache_data["pattern"] = pattern

    monkeypatch.setattr(
        "services.user.user_repository.get_by_id",
        mock_get_by_id,
    )

    monkeypatch.setattr(
        "services.user.user_repository.delete",
        mock_delete,
    )

    monkeypatch.setattr(
        "services.user.delete_cache_pattern",
        mock_delete_cache_pattern,
    )

    await UserService.delete_user(
        5,
        db_session,
        other_user,
    )

    assert cache_data["deleted_user"] == user
    assert cache_data["pattern"] == "users:*"


@pytest.mark.asyncio
async def test_delete_user_not_found(monkeypatch, db_session, current_user):
    def mock_get_by_id(db, user_id):
        return None

    monkeypatch.setattr(
        "services.user.user_repository.get_by_id",
        mock_get_by_id,
    )

    with pytest.raises(NotFoundException) as exc:
        await UserService.delete_user(
            999,
            db_session,
            current_user,
        )

    assert str(exc.value) == "User not found"
