from enums.stock_movement_type import StockMovementType
from models.product import Item
from models.stock_movement import StockMovement


def test_create_stock_movement_in(client, auth_headers, current_user, db_session):
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
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["product_id"] == product1.id
    assert response.json()["user_id"] == current_user.id
    assert response.json()["type"] == "IN"
    assert response.json()["quantity"] == 20
    assert response.json()["note"] == "This is test"

    db_session.refresh(product1)
    assert product1.stock_quantity == 30


def test_create_stock_movement_out(
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
        headers=auth_headers,
    )

    assert response.status_code == 201

    db_session.refresh(product)
    assert product.stock_quantity == 30


def test_create_stock_movement_out_insufficient_stock(
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
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert "Not enough products" in response.json()["detail"]

    db_session.refresh(product)
    assert product.stock_quantity == 5


def test_create_stock_movement_invalid_quantity(
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
        headers=auth_headers,
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
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def get_all_stock_movements(client, auth_headers, db_session, current_user):
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

    assert len(data) == 2

    assert data[0]["product_id"] == product1.id
    assert data[0]["user_id"] == current_user.id
    assert data[0]["type"] == "IN"
    assert data[0]["quantity"] == 20
    assert data[0]["note"] == "New products"

    assert data[1]["product_id"] == product1.id
    assert data[1]["user_id"] == current_user.id
    assert data[1]["type"] == "OUT"
    assert data[1]["quantity"] == 10
    assert data[1]["note"] == "Out products"
