from datetime import datetime, timezone

import pytest

from enums.stock_movement_type import StockMovementType
from models.product import Item
from models.stock_movement import StockMovement
from services.stock_movement import StockMovementService


@pytest.mark.asyncio
async def test_create_stock_movement_in(client, auth_headers, current_user, db_session):
    product1 = Item(name="TestProduct1", price=100, stock_quantity=10)

    db_session.add(product1)
    db_session.commit()
    db_session.refresh(product1)

    response = client.post(
        "/stock-movements",
        json={
            "product_id": product1.id,
            "type": StockMovementType.IN,
            "quantity": 20,
            "note": "This is test",
        },
        headers={
            **auth_headers,
            "Idempotency-Key": "test_stock_in_1",
        },
    )

    assert response.status_code == 201
    assert response.json()["product_id"] == product1.id
    assert response.json()["user_id"] == current_user.id
    assert response.json()["type"] == StockMovementType.IN
    assert response.json()["quantity"] == 20
    assert response.json()["note"] == "This is test"

    db_session.refresh(product1)
    assert product1.stock_quantity == 30


@pytest.mark.asyncio
async def test_create_stock_movement_out(
    client,
    auth_headers,
    db_session,
):
    product = Item(name="TestProduct", price=100, stock_quantity=50)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.post(
        "/stock-movements",
        json={
            "product_id": product.id,
            "type": StockMovementType.OUT,
            "quantity": 20,
            "note": "Stock outgoing",
        },
        headers={
            **auth_headers,
            "Idempotency-Key": "test_stock_out_1",
        },
    )

    assert response.status_code == 201

    db_session.refresh(product)
    assert product.stock_quantity == 30


@pytest.mark.asyncio
async def test_create_stock_movement_idempotency(client, auth_headers, db_session):
    product = Item(
        name="TestProduct",
        price=100,
        stock_quantity=50,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    headers = {
        **auth_headers,
        "Idempotency-Key": "test_stock_idempotency_1",
    }

    data = {
        "product_id": product.id,
        "type": StockMovementType.OUT,
        "quantity": 20,
        "note": "Stock outgoing",
    }

    first_response = client.post("/stock-movements", json=data, headers=headers)

    second_response = client.post("/stock-movements", json=data, headers=headers)

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    assert first_response.json()["id"] == second_response.json()["id"]

    db_session.refresh(product)

    assert product.stock_quantity == 30


@pytest.mark.asyncio
async def test_create_stock_movement_out_insufficient_stock(
    client,
    auth_headers,
    db_session,
):
    product = Item(name="TestProduct", price=100, stock_quantity=5)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.post(
        "/stock-movements",
        json={
            "product_id": product.id,
            "type": StockMovementType.OUT,
            "quantity": 10,
            "note": "Too much stock",
        },
        headers={
            **auth_headers,
            "Idempotency-Key": "test_invalid_quantity_out_1",
        },
    )

    assert response.status_code == 400
    assert "Not enough products" in response.json()["detail"]

    db_session.refresh(product)
    assert product.stock_quantity == 5


@pytest.mark.asyncio
async def test_create_stock_movement_invalid_quantity(
    client,
    auth_headers,
    db_session,
):
    product = Item(name="TestProduct", price=100, stock_quantity=10)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.post(
        "/stock-movements",
        json={
            "product_id": product.id,
            "type": StockMovementType.IN,
            "quantity": 0,
            "note": "Invalid quantity",
        },
        headers={**auth_headers, "Idempotency-Key": "test_invalid_quantity_IN_1"},
    )

    assert response.status_code == 400
    assert "Quantity must be greater than zero" in response.json()["detail"]


def test_create_stock_movement_product_not_found(
    client,
    auth_headers,
):
    response = client.post(
        "/stock-movements",
        json={
            "product_id": 999999,
            "type": StockMovementType.IN,
            "quantity": 10,
            "note": "Missing product",
        },
        headers={**auth_headers, "Idempotency-Key": "test_product_not_found_1"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@pytest.mark.asyncio
async def test_get_all_stock_movements(client, auth_headers, db_session, current_user):
    product1 = Item(name="TestProduct1", price=100, stock_quantity=10)

    db_session.add(product1)
    db_session.commit()
    db_session.refresh(product1)

    stock_movement_in = StockMovement(
        product_id=product1.id,
        user_id=current_user.id,
        type=StockMovementType.IN,
        quantity=20,
        note="New products",
    )

    stock_movement_out = StockMovement(
        product_id=product1.id,
        user_id=current_user.id,
        type=StockMovementType.OUT,
        quantity=10,
        note="Out products",
    )

    db_session.add_all([stock_movement_in, stock_movement_out])
    db_session.commit()

    response = client.get("/stock-movements", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert len(data["movements"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] == 2
    assert data["total_pages"] == 1

    assert data["movements"][0]["product_id"] == product1.id
    assert data["movements"][0]["user_id"] == current_user.id
    assert data["movements"][0]["type"] == "IN"
    assert data["movements"][0]["quantity"] == 20
    assert data["movements"][0]["note"] == "New products"

    assert data["movements"][1]["product_id"] == product1.id
    assert data["movements"][1]["user_id"] == current_user.id
    assert data["movements"][1]["type"] == "OUT"
    assert data["movements"][1]["quantity"] == 10
    assert data["movements"][1]["note"] == "Out products"


@pytest.mark.asyncio
async def test_get_all_stock_movements_pagination(
    client, auth_headers, db_session, current_user
):
    product = Item(
        name="TestProduct",
        price=100,
        stock_quantity=100,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    for i in range(15):
        movement = StockMovement(
            product_id=product.id,
            user_id=current_user.id,
            type=StockMovementType.IN,
            quantity=i + 1,
            note=f"Movement {i + 1}",
        )
        db_session.add(movement)

    db_session.commit()

    response = client.get(
        "/stock-movements?page=2&limit=10",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 10
    assert data["total"] == 15
    assert data["total_pages"] == 2
    assert len(data["movements"]) == 5


@pytest.mark.asyncio
async def test_get_stock_movement_per_user(
    client, auth_headers, db_session, current_user
):
    product = Item(
        name="TestProduct",
        price=100,
        stock_quantity=20,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    movement = StockMovement(
        product_id=product.id,
        user_id=current_user.id,
        type=StockMovementType.IN,
        quantity=10,
        note="Test movement",
    )

    db_session.add(movement)
    db_session.commit()
    db_session.refresh(movement)

    response = client.get(
        f"/stock-movements/user/{current_user.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["product_id"] == product.id
    assert data[0]["user_id"] == current_user.id
    assert data[0]["type"] == StockMovementType.IN
    assert data[0]["quantity"] == 10
    assert data[0]["note"] == "Test movement"


@pytest.mark.asyncio
async def test_get_stock_history_user_from_cache(monkeypatch, db_session):
    cached_movements = [
        {
            "id": 1,
            "product_id": 1,
            "product": {
                "id": 1,
                "name": "TestProduct",
            },
            "user_id": 5,
            "quantity": 10,
            "type": StockMovementType.IN,
            "created_at": datetime.now(timezone.utc),
        }
    ]

    async def mock_get_cache(key):
        return cached_movements

    # ovdje koristim kao funkciju da privremeno promijenim ponasanje neke funkcije koju testiram
    # u stvari laziram Redis
    monkeypatch.setattr(
        "services.stock_movement.get_cache",
        mock_get_cache,
    )

    def mock_get_by_user_id(db, user_id):
        pytest.fail("Repository should not be called when cache exists")

    monkeypatch.setattr(
        "services.stock_movement.stock_movement_repository.get_by_user_id",
        mock_get_by_user_id,
    )

    result = await StockMovementService.get_stock_history_user(5, db_session)

    assert len(result) == 1
    assert result[0].id == 1


@pytest.mark.asyncio
async def test_get_stock_history_user_cache_miss(
    monkeypatch, db_session, stock_movement
):
    async def mock_get_cache(key):
        return None

    cache_data = {}

    async def mock_set_cache(key, value, expire):
        cache_data["key"] = key
        cache_data["value"] = value
        cache_data["expire"] = expire

    monkeypatch.setattr(
        "services.stock_movement.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.stock_movement.set_cache",
        mock_set_cache,
    )

    def mock_get_by_user_id(db, user_id):
        return [stock_movement]

    monkeypatch.setattr(
        "services.stock_movement.stock_movement_repository.get_by_user_id",
        mock_get_by_user_id,
    )

    result = await StockMovementService.get_stock_history_user(5, db_session)

    assert len(result) == 1
    assert cache_data["key"] == "stock_movements:user:5"
    assert cache_data["expire"] == 300


@pytest.mark.asyncio
async def test_get_stock_history_user_empty(monkeypatch, db_session):
    async def mock_get_cache(key):
        return None

    def mock_get_by_user_id(db, user_id):
        return []

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr(
        "services.stock_movement.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.stock_movement.set_cache",
        mock_set_cache,
    )

    monkeypatch.setattr(
        "services.stock_movement.stock_movement_repository.get_by_user_id",
        mock_get_by_user_id,
    )

    result = await StockMovementService.get_stock_history_user(999, db_session)

    assert result == []


@pytest.mark.asyncio
async def test_get_stock_movement_per_product(
    client, auth_headers, db_session, current_user
):
    product = Item(
        name="TestProduct",
        price=100,
        stock_quantity=20,
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    movement = StockMovement(
        product_id=product.id,
        user_id=current_user.id,
        type=StockMovementType.IN,
        quantity=10,
        note="Test movement",
    )

    db_session.add(movement)
    db_session.commit()
    db_session.refresh(movement)

    response = client.get(
        f"/stock-movements/product/{product.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["product_id"] == product.id
    assert data[0]["user_id"] == current_user.id
    assert data[0]["type"] == StockMovementType.IN
    assert data[0]["quantity"] == 10
    assert data[0]["note"] == "Test movement"


@pytest.mark.asyncio
async def test_get_stock_history_product_from_cache(monkeypatch, db_session):
    cached_movements = [
        {
            "id": 1,
            "product_id": 1,
            "product": {
                "id": 1,
                "name": "TestProduct",
            },
            "user_id": 5,
            "quantity": 10,
            "type": StockMovementType.IN,
            "created_at": datetime.now(timezone.utc),
        }
    ]

    async def mock_get_cache(key):
        return cached_movements

    # ovdje koristim kao funkciju da privremeno promijenim ponasanje neke funkcije koju testiram
    # u stvari laziram Redis
    monkeypatch.setattr(
        "services.stock_movement.get_cache",
        mock_get_cache,
    )

    def mock_get_by_product_id(db, product_id):
        pytest.fail("Repository should not be called when cache exists")

    monkeypatch.setattr(
        "services.stock_movement.stock_movement_repository.get_by_product_id",
        mock_get_by_product_id,
    )

    result = await StockMovementService.get_stock_history_product(5, db_session)

    assert len(result) == 1
    assert result[0].id == 1


@pytest.mark.asyncio
async def test_get_stock_history_product_cache_miss(
    monkeypatch, db_session, stock_movement
):
    async def mock_get_cache(key):
        return None

    cache_data = {}

    async def mock_set_cache(key, value, expire):
        cache_data["key"] = key
        cache_data["value"] = value
        cache_data["expire"] = expire

    monkeypatch.setattr(
        "services.stock_movement.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.stock_movement.set_cache",
        mock_set_cache,
    )

    def mock_get_by_product_id(db, product_id):
        return [stock_movement]

    monkeypatch.setattr(
        "services.stock_movement.stock_movement_repository.get_by_product_id",
        mock_get_by_product_id,
    )

    result = await StockMovementService.get_stock_history_product(5, db_session)

    assert len(result) == 1
    assert cache_data["key"] == "stock_movements:product:5"
    assert cache_data["expire"] == 300


@pytest.mark.asyncio
async def test_get_stock_history_product_empty(monkeypatch, db_session):
    async def mock_get_cache(key):
        return None

    def mock_get_by_product_id(db, prodcut_id):
        return []

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr(
        "services.stock_movement.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.stock_movement.set_cache",
        mock_set_cache,
    )

    monkeypatch.setattr(
        "services.stock_movement.stock_movement_repository.get_by_product_id",
        mock_get_by_product_id,
    )

    result = await StockMovementService.get_stock_history_product(999, db_session)

    assert result == []
