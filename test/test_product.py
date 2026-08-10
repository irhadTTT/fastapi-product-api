import pytest

from enums.sort import SortField, SortOrder
from models.category import Category
from models.product import Item
from services.product import ProductService


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


@pytest.mark.asyncio
async def test_get_items_cache_miss_with_filters(monkeypatch, db_session, other_user):
    cache_data = {}

    async def mock_get_cache(key):
        return None

    async def mock_set_cache(key, value, expire):
        cache_data["key"] = key
        cache_data["value"] = value
        cache_data["expire"] = expire

    monkeypatch.setattr(
        "services.product.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.product.set_cache",
        mock_set_cache,
    )

    result = await ProductService.get_items(
        db_session,
        q="phone",
        min_price=10,
        max_price=1000,
        sort_by=SortField.price,
        order=SortOrder.desc,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.page == 1
    assert result.limit == 10
    assert cache_data["expire"] == 300


@pytest.mark.asyncio
async def test_get_items_sort_by_created_at(db_session, other_user):
    result = await ProductService.get_items(
        db_session,
        q=None,
        min_price=None,
        max_price=None,
        sort_by=SortField.created_at,
        order=SortOrder.desc,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.page == 1
    assert result.limit == 10


@pytest.mark.asyncio
async def test_get_items_sort_by_name(db_session, other_user):
    result = await ProductService.get_items(
        db_session,
        q=None,
        min_price=None,
        max_price=None,
        sort_by=SortField.name,
        order=SortOrder.asc,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.page == 1
    assert result.limit == 10


@pytest.mark.asyncio
async def test_get_items_from_cache(monkeypatch, db_session, other_user):
    cached_data = {
        "products": [],
        "page": 1,
        "limit": 10,
        "total": 0,
        "total_pages": 0,
    }

    async def mock_get_cache(key):
        return cached_data

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr(
        "services.product.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.product.set_cache",
        mock_set_cache,
    )

    result = await ProductService.get_items(
        db_session,
        q=None,
        min_price=None,
        max_price=None,
        sort_by=None,
        order=None,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.page == 1
    assert result.limit == 10
    assert result.total == 0
    assert result.total_pages == 0
    assert result.products == []


@pytest.mark.asyncio
async def test_get_items_admin_with_filters(db_session, admin_user):
    admin_user.role = "admin"
    db_session.commit()

    product1 = Item(
        name="iPhone",
        price=500,
        owner_id=admin_user.id,
    )

    product2 = Item(
        name="Laptop",
        price=1500,
        owner_id=admin_user.id,
    )

    db_session.add_all([product1, product2])
    db_session.commit()

    result = await ProductService.get_items(
        db_session,
        q="phone",
        min_price=100,
        max_price=1000,
        sort_by=SortField.price,
        order=SortOrder.desc,
        page=1,
        limit=10,
        current_user=admin_user,
    )

    assert result.total == 1
    assert result.products[0].name == "iPhone"


@pytest.mark.asyncio
async def test_get_items_with_all_filters(db_session, other_user, monkeypatch):
    async def mock_get_cache(key):
        return None

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr(
        "services.product.get_cache",
        mock_get_cache,
    )

    monkeypatch.setattr(
        "services.product.set_cache",
        mock_set_cache,
    )

    product1 = Item(name="iPhone 16", price=1000, owner_id=other_user.id)

    product2 = Item(name="Samsung Galaxy", price=1500, owner_id=other_user.id)

    product3 = Item(name="iPhone 15", price=500, owner_id=other_user.id)

    db_session.add_all([product1, product2, product3])
    db_session.commit()

    result = await ProductService.get_items(
        db=db_session,
        q="iPhone",
        min_price=600,
        max_price=1200,
        sort_by=SortField.price,
        order=SortOrder.asc,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.total == 1
    assert len(result.products) == 1
    assert result.products[0].name == "iPhone 16"
    assert result.products[0].price == 1000


@pytest.mark.asyncio
async def test_get_items_pagination(
    db_session,
    other_user,
    monkeypatch,
):
    async def mock_get_cache(key):
        return None

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr("services.product.get_cache", mock_get_cache)
    monkeypatch.setattr("services.product.set_cache", mock_set_cache)

    products = [
        Item(name=f"Product {i}", price=100 + i, owner_id=other_user.id)
        for i in range(1, 6)
    ]

    db_session.add_all(products)
    db_session.commit()

    result = await ProductService.get_items(
        db=db_session,
        q=None,
        min_price=None,
        max_price=None,
        sort_by=None,
        order=None,
        page=2,
        limit=2,
        current_user=other_user,
    )

    assert result.page == 2
    assert result.limit == 2
    assert result.total == 5
    assert result.total_pages == 3
    assert len(result.products) == 2


@pytest.mark.asyncio
async def test_get_items_sort_by_price_desc(
    db_session,
    other_user,
    monkeypatch,
):
    async def mock_get_cache(key):
        return None

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr("services.product.get_cache", mock_get_cache)
    monkeypatch.setattr("services.product.set_cache", mock_set_cache)

    product1 = Item(name="Cheap Product", price=100, owner_id=other_user.id)

    product2 = Item(name="Expensive Product", price=500, owner_id=other_user.id)

    db_session.add_all([product1, product2])
    db_session.commit()

    result = await ProductService.get_items(
        db=db_session,
        q=None,
        min_price=None,
        max_price=None,
        sort_by=SortField.price,
        order=SortOrder.desc,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.products[0].name == "Expensive Product"
    assert result.products[1].name == "Cheap Product"


@pytest.mark.asyncio
async def test_get_items_sort_by_name_desc(
    db_session,
    other_user,
    monkeypatch,
):
    async def mock_get_cache(key):
        return None

    async def mock_set_cache(key, value, expire):
        pass

    monkeypatch.setattr("services.product.get_cache", mock_get_cache)
    monkeypatch.setattr("services.product.set_cache", mock_set_cache)

    product1 = Item(name="Apple", price=100, owner_id=other_user.id)

    product2 = Item(name="Samsung", price=200, owner_id=other_user.id)

    db_session.add_all([product1, product2])
    db_session.commit()

    result = await ProductService.get_items(
        db=db_session,
        q=None,
        min_price=None,
        max_price=None,
        sort_by=SortField.name,
        order=SortOrder.desc,
        page=1,
        limit=10,
        current_user=other_user,
    )

    assert result.products[0].name == "Samsung"
    assert result.products[1].name == "Apple"


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
