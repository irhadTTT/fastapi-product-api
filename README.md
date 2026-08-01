# StockFlow API 🚀

A modern inventory management REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic and Docker.
Designed as a scalable backend foundation for future stock management features such as inventory tracking, suppliers, orders and reporting.

---

## Features 🚀

s* JWT-based user authentication
* Secure password hashing with bcrypt
* Role-based authorization (Admin/User)
* Protected user-specific resources
* Admin management capabilities
* Category management
* Product CRUD operations
* Product image upload and management
* Image validation and upload size limits
* Automatic image cleanup when deleting products
* Product filtering and advanced searching
* Multi-field product sorting
* Pagination support
* PostgreSQL database integration
* Database migrations with Alembic
* SQLAlchemy ORM for database operations
* Pydantic schema validation
* Dockerized development environment
* Swagger/OpenAPI interactive documentation
* Add automated testing with Pytest for authentication and category features
<img width="1895" height="1032" alt="Screenshot 2026-07-31 210242" src="https://github.com/user-attachments/assets/b09d6660-4d64-453c-9caf-6b5a92bce514" />
* Centralized exception handling with custom API exceptions
* Authentication rate limiting to prevent brute-force login attempts
* Repository Pattern for database operations
* Code quality improvements with Ruff linting and formatting

## Tech Stack

* Python
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic (Database migrations)
* Pydantic (Data validation)
* JWT Authentication
* bcrypt (Password hashing)
* Docker & Docker Compose
* Swagger / OpenAPI Documentation

## Installation

### Clone repository

git clone ...

### Start services

docker compose up --build

## Database migrations

alembic upgrade head

## API Documentation

Open:

http://localhost:8000/docs

## Admin account (development)
```text
For testing admin endpoints, use the default admin account:

Username: admin
Password: admin123
```
<img width="1918" height="1002" alt="Screenshot 2026-07-31 212757" src="https://github.com/user-attachments/assets/dc11b361-fa3e-4303-9dfc-ade43d34c58c" />


## Docker Services

- FastAPI container
- PostgreSQL container

## 📦 Product Management

* Create products
* Retrieve all products
* Retrieve product by ID
* Update product information
* Delete products
* Manage product data through REST API endpoints

## 🔐 Authentication

* User registration
* User login
* JWT-based authentication
* Secure password hashing using bcrypt
* Protected API routes

## 🗄️ Database

* SQLite database integration
* SQLAlchemy ORM
* Database models
* Structured data access

## ✅ Data Validation

* Request validation using Pydantic
* Response schemas
* Automatic API validation

## 📖 API Documentation

* Automatic Swagger UI documentation
* OpenAPI support
* Interactive API testing

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite

## Authentication & Security

* JWT
* bcrypt
* OAuth2 authentication flow

## Tools

* Uvicorn
* Git
* GitHub
* Swagger UI

---

# 🏗️ Architecture

The project follows a layered backend architecture:

```text
                         Client
                            |
                            |
                            ▼

                 ┌──────────────────┐
                 │      FastAPI     │
                 │      Routes      │
                 │    (Routers)     │
                 └────────┬─────────┘
                          |
                          ▼

                 ┌──────────────────┐
                 │     Schemas      │
                 │     Pydantic     │
                 │ Request/Response │
                 └────────┬─────────┘
                          |
                          ▼

                 ┌──────────────────┐
                 │    Repository    │
                 │      Layer       │
                 │  Data Access     │
                 │ UserRepository   │
                 └────────┬─────────┘
                          |
                          ▼

                 ┌──────────────────┐
                 │   SQLAlchemy     │
                 │      Models      │
                 │    ORM Layer     │
                 │ User, Post, ...  │
                 └────────┬─────────┘
                          |
                          ▼

                 ┌──────────────────┐
                 │    PostgreSQL    │
                 │     Database     │
                 └──────────────────┘


                 ┌──────────────────┐
                 │     Alembic      │
                 │    Migrations    │
                 └────────┬─────────┘
                          |
                          ▼
                 ┌──────────────────┐
                 │     Database     │
                 │     Schema       │
                 └──────────────────┘


                 ┌──────────────────┐
                 │      Docker      │
                 │ Docker Compose   │
                 │ App + Database   │
                 └──────────────────┘
```

---

# 📂 Project Structure
```text
fastapi-product-api/
│
├── main.py
├── database.py
├── dependencies.py
│
├── core/
│   ├── __init__.py
│   └── exceptions.py
│
├── models/
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   └── category.py
│
├── schemas/
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   ├── auth.py
│   └── category.py
│
├── repositories/
│   ├── __init__.py
│   ├── product_repository.py
│   ├── user_repository.py
│   └── category_repository.py
│
├── router/
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   ├── auth.py
│   └── category.py
│
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_products.py
│   └── test_categories.py
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env
└── README.md
```

---

# ⚙️ Installation & Setup

## Clone Repository

```bash
git clone https://github.com/irhadTTT/fastapi-product-api.git

cd fastapi-product-api
```

# 🔑 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@postgres:5432/database_name
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```


# 📖 API Documentation

FastAPI automatically provides interactive documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔌 API Endpoints

## Authentication

## Authentication

| Method | Endpoint        | Description        |
| ------ | --------------- | ------------------ |
| POST   | `/auth/login`   | User login         |
| POST   | `/auth/register`| Register user      |
| GET    | `/auth/me`      | Get current user   |

---

## Users

| Method | Endpoint                          | Description              |
| ------ | --------------------------------- | ------------------------ |
| GET    | `/users/`                         | Get users                |
| POST   | `/users/`                         | Create user              |
| DELETE | `/users/{user_id}`                | Delete user              |
| PUT    | `/users/{user_id}/role`           | Change user role         |
| POST   | `/users/make-first-admin`         | Make first admin         |
| PUT    | `/users/{user_id}/reset-password` | Reset password           |

---

## Products

| Method | Endpoint                         | Description              |
| ------ | -------------------------------- | ------------------------ |
| GET    | `/products/`                     | Get products             |
| POST   | `/products/`                     | Create product           |
| GET    | `/products/{item_id}`            | Get product details      |
| PUT    | `/products/{item_id}`            | Update product            |
| DELETE | `/products/{item_id}`            | Delete product            |
| POST   | `/products/{product_id}/image`   | Upload product image     |

---

## Categories

| Method | Endpoint                         | Description              |
| ------ | -------------------------------- | ------------------------ |
| GET    | `/categories/`                   | Get categories           |
| POST   | `/categories/`                   | Create category          |
| DELETE | `/categories/{category_id}`      | Delete category          |

---

## Health Check

| Method | Endpoint   | Description  |
| ------ | ---------- | ------------ |
| GET    | `/health`  | Health check |

---

# 🔄 Request Flow

1. Client sends HTTP request.
2. FastAPI receives the request.
3. Pydantic validates input data.
4. Application logic processes the request.
5. SQLAlchemy communicates with the database.
6. API returns JSON response.

---

# 🔒 Security

Implemented security features:

* JWT authentication and authorization
* Password hashing using bcrypt
* Protected API routes
* Role-based access control (User/Admin)
* Input validation with Pydantic schemas
* Environment-based configuration using `.env`
* Secure password reset functionality
---

## 🚀 Future Improvements

Possible improvements:

- Refresh token implementation
- Cloud deployment
- Automated test coverage improvements
- Database optimization and indexing

---

# 👨‍💻 Author

**Irhad Kunovac**

GitHub:
https://github.com/irhadTTT

---

# 📄 License
This project is licensed under the MIT License.
