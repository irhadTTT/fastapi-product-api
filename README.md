# StockFlow API 🚀

A scalable inventory management REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic and Docker.

StockFlow is a backend system designed with a clean layered architecture using Routers, Services and Repository patterns. It provides secure user authentication, role-based access control, product and category management, inventory tracking and stock movement history.

The API includes email verification, protected resources, advanced product searching, filtering, sorting, pagination, image management and database migration support.

Built with production practices in mind, including centralized exception handling, validation, automated code quality checks and a Dockerized development environment.

---

## Features 🚀


### Authentication & Authorization
* JWT-based user authentication
* Secure password hashing with bcrypt
* Email verification system with verification links
* Role-based authorization (Admin/User)
* Protected user-specific resources
* Authentication rate limiting to prevent brute-force login attempts
* Admin management capabilities

## Logging

The application uses structured logging.

Logs include:
* successful requests
* authentication events
* database operations
* cache operations
* validation errors
* permission errors

Log levels:
- INFO: successful operations and important application events
- WARNING: failed validations, missing resources, unauthorized actions
- DEBUG: cache hits, cache updates, cache invalidation details

### Product & Category Management
* Category management
* Product CRUD operations
* Product image upload and management
* Image validation and upload size limits
* Automatic image cleanup when deleting products
* Product filtering and advanced searching
* Multi-field product sorting
* Pagination support

### Inventory & Stock Management
* Stock movement management (IN/OUT operations)
* Automatic inventory quantity updates after stock movements
* Stock movement history tracking
* Protected stock operations with role-based permissions
* Inventory transaction records with notes and timestamps

### Architecture & Backend Design
* Layered architecture with Router, Service and Repository layers
* Repository Pattern for database operations
* Service layer for business logic separation
* SQLAlchemy ORM for database operations
* Pydantic schema validation
* Centralized exception handling with custom API exceptions

### Database & Infrastructure
* PostgreSQL database integration
* Database migrations with Alembic
* Dockerized development environment
* Docker Compose setup for application and database

### Background Tasks & Async Processing
* Background Tasks & Async Processing
* Celery integration for asynchronous background jobs
* Redis used as Celery message broker and result backend
* Asynchronous email delivery without blocking API requests
* Background email verification task processing
* Improved API responsiveness by moving long-running tasks to workers
* Scalable worker-based task execution architecture

## Caching & Performance
- Redis integration for API response caching
- Async Redis operations for improved performance
- Cache management with configurable expiration times (TTL)
- Cached frequently accessed resources (Products, Users, Categories, Stock Movements)
- Automatic cache invalidation support for data updates

### API Documentation & Quality
* Swagger/OpenAPI interactive documentation
* Automated testing with Pytest for authentication and category features
* Code quality improvements with Ruff linting and formatting
<img width="1895" height="1032" alt="Screenshot 2026-07-31 210242" src="https://github.com/user-attachments/assets/b09d6660-4d64-453c-9caf-6b5a92bce514" />

### API Quality & CI/CD
* Automated testing with Pytest
* CI pipeline for automated checks
* Code quality checks with Ruff
* Swagger/OpenAPI documentation

## Tech Stack

### Backend
* Python
* FastAPI
* SQLAlchemy ORM
* Pydantic
* PostgreSQL
* Alembic (Database migrations)
* Background Processing
* Celery
* Redis Message Broker
* Async Task Workers

### Authentication & Security
* JWT Authentication
* bcrypt (Password hashing)
* Role-Based Access Control (RBAC)
* Authentication rate limiting
* Protected API routes

### Architecture & Development
* Service Layer Architecture
* Repository Pattern
* Dependency Injection (FastAPI Dependencies)
* Custom Exception Handling

### File & Email Services
* File upload handling
* Image validation and management
* Email verification system

### Testing & Code Quality
* Pytest
* Ruff (Linting and Formatting)

### Infrastructure & Documentation
* Docker
* Docker Compose
* Swagger / OpenAPI Documentation
* Redis container
* Celery worker process
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

# 🏗️ Architecture

The project follows a layered backend architecture:

```text
                               Client
                                |
                                |
                                ▼

                    ┌────────────────────┐
                    │      FastAPI       │
                    │      Routers       │
                    │                    │
                    │ auth.py            │
                    │ user.py            │
                    │ product.py         │
                    │ category.py        │
                    │ stock_movement.py  │
                    │                    │
                    │ Request handling   │
                    │ Response handling  │
                    └─────────┬──────────┘
                              |
                              |
                              ▼

                    ┌────────────────────┐
                    │      Schemas       │
                    │      Pydantic      │
                    │                    │
                    │ Request Models     │
                    │ Response Models    │
                    │ Validation         │
                    │ Serialization      │
                    └─────────┬──────────┘
                              |
                              |
                              ▼

                    ┌────────────────────┐
                    │   Service Layer    │
                    │  Business Logic    │
                    │                    │
                    │ AuthService        │
                    │ UserService        │
                    │ ProductService     │
                    │ CategoryService    │
                    │ StockMovementService│
                    │                    │
                    │ - permissions      │
                    │ - stock rules      │
                    │ - email verification│
                    │ - transactions     │
                    │ - cache handling   │
                    └───────┬───────┬────┘
                            |       |
                            |       |
                            ▼       ▼

              ┌────────────────┐   ┌────────────────┐
              │ Repository     │   │ Redis Cache    │
              │ Layer          │   │                │
              │                │   │ Cache Service  │
              │ UserRepository │   │                │
              │ ProductRepository│ │ GET / SET      │
              │ CategoryRepository│ │ DELETE        │
              │ StockMovementRepository│ TTL        │
              │                │   │ Expiration     │
              │ CRUD only      │   └────────────────┘
              │ No business    │
              │ logic          │
              └───────┬────────┘
                      |
                      |
                      ▼

              ┌────────────────┐
              │   SQLAlchemy   │
              │       ORM      │
              │                │
              │ User           │
              │ Product        │
              │ Category       │
              │ StockMovement  │
              └───────┬────────┘
                      |
                      |
                      ▼

              ┌────────────────┐
              │   PostgreSQL   │
              │    Database    │
              └────────────────┘



              Supporting Infrastructure


        ┌────────────────────┐
        │      Security      │
        │                    │
        │ JWT Authentication │
        │ Password Hashing   │
        │ bcrypt             │
        │ Role Permissions   │
        │ Admin/User Access  │
        └────────────────────┘



        ┌────────────────────┐
        │   Dependencies     │
        │                    │
        │ get_current_user   │
        │ get_admin_user     │
        │ Database Session   │
        │ Dependency Inject. │
        └────────────────────┘



        ┌────────────────────┐
        │       Core         │
        │                    │
        │ Configuration      │
        │ Custom Exceptions  │
        │ Email Service      │
        │ Logging            │
        │ Application Utils  │
        └────────────────────┘



        ┌────────────────────┐
        │      Redis         │
        │     Caching        │
        │                    │
        │ Cache Service      │
        │ TTL Management     │
        │ Cache Invalidation │
        │ Performance Layer  │
        └────────────────────┘



        ┌────────────────────┐
        │      Alembic       │
        │    Migrations      │
        │                    │
        │ Schema Versioning  │
        │ Database Changes   │
        │ Migration History  │
        └─────────┬──────────┘
                  |
                  ▼

        ┌────────────────────┐
        │ Database Schema    │
        └────────────────────┘



        ┌────────────────────┐
        │      Docker        │
        │                    │
        │ Dockerfile         │
        │ Docker Compose     │
        │                    │
        │ FastAPI Container  │
        │ PostgreSQL         │
        │ Redis Container    │
        └────────────────────┘



        ┌────────────────────┐
        │        CI/CD       │
        │                    │
        │ GitHub Actions     │
        │ Automated Tests    │
        │ Docker Build       │
        │ Code Quality       │
        └────────────────────┘
```

---

# 📂 Project Structure
```text
StockFlow-API/
│
├── main.py
├── database.py
├── dependencies.py
│
├── core/
│   ├── __init__.py
│   ├── security.py
│   ├── exceptions.py
│   └── config.py
│
├── enums/
│   ├── __init__.py
│   ├── sort.py
│   └── stock_movement_type.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   └── stock_movement.py
│
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   ├── auth.py
│   ├── product.py
│   ├── category.py
│   └── stock_movement.py
│
├── repositories/
│   ├── __init__.py
│   ├── user_repository.py
│   ├── product_repository.py
│   ├── category_repository.py
│   └── stock_movement_repository.py
│
├── services/
│   ├── __init__.py
│   ├── auth.py
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   └── stock_movement.py
│
├── router/
│   ├── __init__.py
│   ├── auth.py
│   ├── user.py
│   ├── product.py
│   ├── category.py
│   └── stock_movement.py
│
├── migrations/
│   ├── versions/
│   │   └── xxxx_create_tables.py
│   │
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_products.py
│   ├── test_categories.py
│   └── test_stock_movements.py
│
├── uploads/
│   └── products/
│       └── images
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
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

SECRET_KEY=your_long_random_secret_key
ALGORITHM=HS256

# Email verification
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_FROM_NAME=StockFlow
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

# Frontend redirect URL after email verification
FRONTEND_URL=https://your-frontend-url.com
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

---
---

## Stock Management

| Method | Endpoint                              | Description                         |
| ------ | ------------------------------------ | ----------------------------------- |
| POST   | `/stock-movements/`                  | Create stock movement (IN / OUT)    |
| GET    | `/stock-movements/`                  | Get all stock movements history     |
| GET    | `/stock-movements/product/{id}`      | Get stock history by product        |
| GET    | `/stock-movements/user/{id}`         | Get stock movements by user         |

---

### Stock Movement Types

Stock changes are handled through movement records:

- `IN` → Adds quantity to product stock
- `OUT` → Removes quantity from product stock

Each stock movement contains:

- Product reference
- User who performed the action
- Movement type
- Quantity changed
- Optional note
- Created timestamp

---

## Health Check

| Method | Endpoint   | Description  |
| ------ | ---------- | ------------ |
| GET    | `/health`  | Health check |

---

# 🔄 Request Flow

1. Client sends an HTTP request.
2. FastAPI Router receives the request.
3. Pydantic Schemas validate request data.
4. Service Layer handles business logic and application rules.
5. Repository Layer manages database operations.
6. SQLAlchemy ORM communicates with PostgreSQL database.
7. Database returns the requested data.
8. Service Layer processes the result.
9. FastAPI returns a JSON response to the client.
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
