from models.category import Category
from models.product import Item


def test_create_product(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "Laptop Lenovo",
            "description": "Test laptop",
            "price": 2000,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Laptop Lenovo"
    assert response.json()["price"] == 2000


def test_create_product_unauthorized(client):
    response = client.post("/products/", json={"name": "Laptop Lenovo", "price": 2000})

    assert response.status_code == 401


def test_create_product_invalid_data(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "To",
            "price": -2000,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_product_name_too_long(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "pppppppppppppppppppppppppppppppppppppppppppppppppppppppp",
            "price": 2000,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_product_price_negative(client, auth_headers):
    response = client.post(
        "/products/",
        json={
            "name": "Iphone 16",
            "price": -2000,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_product_saved_to_database(client, auth_headers, db_session):
    response = client.post(
        "/products/",
        json={"name": "Laptop Lenovo", "price": 2000},
        headers=auth_headers,
    )

    assert response.status_code == 201

    product = db_session.query(Item).filter(Item.name == "Laptop Lenovo").first()

    assert product is not None
    assert product.price == 2000


def get_all_products(client, db_session):
    category1 = Category(name="Category1")

    db_session.add(category1)
    db_session.commit()

    product1 = Item(name="TestProduct1", price=100, category_id=category1.id)

    product2 = Item(name="TestProduct2", price=200, category_id=category1.id)

    product3 = Item(name="TestProduct3", price=200, category_id=category1.id)

    db_session.add_all([product1, product2, product3])
    db_session.commit()

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3
    assert data[0]["name"] == "TestProduct1"
    assert data[0]["price"] == 100
    assert data[0]["category_id"] == 1

    assert data[1]["name"] == "TestProduct2"
    assert data[1]["price"] == 200
    assert data[1]["category_id"] == 1

    assert data[2]["name"] == "TestProduct3"
    assert data[2]["price"] == 300
    assert data[2]["category_id"] == 1


def get_product(client, db_session, auth_headers):
    product = Item(name="TestProduct", price=200)

    db_session.add(product)
    db_session.commit()

    response = client.get(f"/products/{product.id}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["name"] == "TestProduct"
    assert response.json()["price"] == 200


def test_get_product_unauthorized(client, db_session):
    product = Item(name="Laptop Lenovo", price=2000)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.get(f"/products/{product.id}")

    assert response.status_code == 401


def test_get_product_not_found(client, auth_headers):
    response = client.get("/products/999999", headers=auth_headers)

    assert response.status_code == 404


def test_get_product_other_user(client, auth_headers, db_session, other_user):
    product = Item(name="Other Laptop", price=2000, owner_id=other_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.get(f"/products/{product.id}", headers=auth_headers)

    assert response.status_code == 403


def test_delete_product(client, auth_headers, db_session, current_user):
    product = Item(name="Laptop Lenovo", price=2000, owner_id=current_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}", headers=auth_headers)

    assert response.status_code == 204

    deleted_product = db_session.query(Item).filter(Item.id == product.id).first()

    assert deleted_product is None


def test_delete_product_unauthorized(client, db_session):
    product = Item(name="Laptop Lenovo", price=2000)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}")

    assert response.status_code == 401


def test_delete_product_forbidden(client, auth_headers, db_session, other_user):
    product = Item(name="Other Laptop", price=2000, owner_id=other_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}", headers=auth_headers)

    assert response.status_code == 403

    product_still_exists = db_session.query(Item).filter(Item.id == product.id).first()

    assert product_still_exists is not None


def test_admin_delete_product(client, admin_auth_headers, db_session, other_user):
    product = Item(name="Other Laptop", price=2000, owner_id=other_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}", headers=admin_auth_headers)

    assert response.status_code == 204

    deleted_product = db_session.query(Item).filter(Item.id == product.id).first()

    assert deleted_product is None


def test_delete_product_not_found(client, auth_headers):
    response = client.delete("/products/999999", headers=auth_headers)

    assert response.status_code == 404


def test_update_product(client, auth_headers, db_session, current_user):
    product = Item(name="Laptop Lenovo", price=2000, owner_id=current_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.put(
        f"/products/{product.id}",
        json={"name": "Laptop Dell", "price": 2500, "category_id": None},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Laptop Dell"
    assert response.json()["price"] == 2500


def test_update_product_forbidden(client, auth_headers, db_session, other_user):
    product = Item(name="Other Laptop", price=2000, owner_id=other_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.put(
        f"/products/{product.id}",
        json={"name": "Hacked Laptop", "price": 1, "category_id": None},
        headers=auth_headers,
    )

    assert response.status_code == 403

    product_after = db_session.query(Item).filter(Item.id == product.id).first()

    assert product_after.name == "Other Laptop"
    assert product_after.price == 2000


def test_admin_update_product(client, admin_auth_headers, db_session, other_user):
    product = Item(name="Other Laptop", price=2000, owner_id=other_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.put(
        f"/products/{product.id}",
        json={"name": "Admin Updated Laptop", "price": 3000, "category_id": None},
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Admin Updated Laptop"
    assert response.json()["price"] == 3000


def test_update_product_not_found(client, auth_headers):
    response = client.put(
        "/products/999999",
        json={"name": "Laptop", "price": 2000, "category_id": None},
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_update_product_unauthorized(client):
    response = client.put(
        "/products/1", json={"name": "Laptop", "price": 2000, "category_id": None}
    )

    assert response.status_code == 401


def test_update_product_invalid_data(client, auth_headers, db_session, current_user):
    product = Item(name="Laptop", price=2000, owner_id=current_user.id)

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.put(
        f"/products/{product.id}",
        json={"name": "ab", "price": -100, "category_id": None},
        headers=auth_headers,
    )

    assert response.status_code == 422
