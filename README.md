# StockFlow API 🚀

A modern inventory management REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic and Docker.
Designed as a scalable backend foundation for future stock management features such as inventory tracking, suppliers, orders and reporting.

---

## Features 🚀

* JWT-based user authentication
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
* Code quality improvements with Ruff linting and formatting
<img width="1918" height="1078" alt="Screenshot 2026-07-31 234138" src="https://github.com/user-attachments/assets/abf771f8-261d-4d2f-8f8a-0c571ed11c73" />


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

              ┌────────────────┐
              │    FastAPI     │
              │     Routes     │
              │    (Router)    │
              └────────┬───────┘
                       |
                       ▼

              ┌────────────────┐
              │    Schemas     │
              │    Pydantic    │
              │ Request/Response│
              └────────┬───────┘
                       |
                       ▼

              ┌────────────────┐
              │  SQLAlchemy    │
              │     Models     │
              │   ORM Layer    │
              └────────┬───────┘
                       |
                       ▼

              ┌────────────────┐
              │    Alembic     │
              │   Migrations   │
              └────────┬───────┘
                       |
                       ▼

              ┌────────────────┐
              │   PostgreSQL   │
              │    Database    │
              └────────────────┘
                       ▲
                       |
                       |
              ┌────────────────┐
              │    Docker      │
              │ Docker Compose │
              └────────────────┘
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
├── models/
│   ├── __init__.py
│   ├── product.py
│   └── user.py
│
├── schemas/
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   └── auth.py
│
├── router/
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   └── auth.py
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env
├── database.sqlite3
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

| Method | Endpoint    | Description       |
| ------ | ----------- | ----------------- |
| POST   | `/register` | Create new user   |
| POST   | `/login`    | Authenticate user |

---

## Products

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| GET    | `/products`      | Get all products    |
| GET    | `/products/{id}` | Get product details |
| POST   | `/products`      | Create product      |
| PUT    | `/products/{id}` | Update product      |
| DELETE | `/products/{id}` | Delete product      |

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

* JWT authentication
* Password hashing with bcrypt
* Protected routes
* Input validation
* Environment-based configuration

---

## 🚀 Future Improvements

Possible improvements:

- Automated testing with Pytest
- API rate limiting
- Refresh token implementation
- Product categories
- Image upload for products
- Pagination and filtering
- Cloud deployment
- CI/CD pipeline

---

# 👨‍💻 Author

**Irhad Kunovac**

GitHub:
https://github.com/irhadTTT

---

# 📄 License
This project is licensed under the MIT License.
