from models.category import Category
from models.product import Item
from models.user import User
from security import hash_password


def test_create_category(client, db_session):
    admin = User(
        username="admin1",
        email="admin1@test.com",
        password=hash_password("admin1"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "admin1", "password": "admin1"}
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/categories",
        json={
            "name": "TestCategory",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_category_exists(client, db_session):
    admin = User(
        username="admin2",
        email="admin2@test.com",
        password=hash_password("admin2"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "admin2", "password": "admin2"}
    )

    token = login_response.json()["access_token"]

    category = Category(name="TestCatgory2")

    db_session.add(category)
    db_session.commit()

    response = client.post(
        "/categories",
        json={
            "name": "TestCatgory2",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Category already exists"


def test_get_all_categories(client, db_session):
    category3 = Category(name="TestCategory3")

    category4 = Category(name="TestCategory4")

    category5 = Category(name="TestCategory5")

    db_session.add_all([category3, category4, category5])
    db_session.commit()

    response = client.get("/categories")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3
    assert data[0]["name"] == "TestCategory3"
    assert data[1]["name"] == "TestCategory4"
    assert data[2]["name"] == "TestCategory5"


def test_delete_category_success(client, db_session):
    admin = User(
        username="admin3",
        email="admin3@test.com",
        password=hash_password("admin3"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()

    categoryTest = Category(name="CategoryTest")

    db_session.add(categoryTest)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "admin3", "password": "admin3"}
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/categories/{categoryTest.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    deleted_category = (
        db_session.query(Category).filter(Category.id == categoryTest.id).first()
    )

    assert deleted_category is None


def test_delete_category_exists(client, db_session):
    admin = User(
        username="admin4",
        email="admin4@test.com",
        password=hash_password("admin4"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "admin4", "password": "admin4"}
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        "/categories/1111111", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"


def test_delete_category_products_exists(client, db_session):
    admin = User(
        username="admin5",
        email="admin5@test.com",
        password=hash_password("admin5"),
        role="admin",
    )

    db_session.add(admin)
    db_session.commit()

    login_response = client.post(
        "/auth/login", data={"username": "admin5", "password": "admin5"}
    )

    token = login_response.json()["access_token"]

    category1 = Category(name="Category1")

    product1 = Item(name="Product1", category=category1)

    db_session.add(category1)
    db_session.add(product1)
    db_session.commit()

    response = client.delete(
        f"/categories/{category1.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot delete category with products"
