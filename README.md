# StockFlow API 🚀

A scalable inventory management REST API built with with FastAPI, PostgreSQL, SQLAlchemy, Alembic, Redis, Celery and Docker.

StockFlow is a backend system designed with a clean layered architecture using Routers, Services and Repository patterns. It provides secure user authentication, role-based access control, product and category management, inventory tracking and stock movement history,caching and asynchronous background processing.

The API includes email verification, protected resources, advanced product searching, filtering, sorting, pagination, image management and database migration support.

Built with production practices in mind, including centralized exception handling, validation, automated code quality checks and a Dockerized development environment.

---

🌐 Live Deployment
Production API

Swagger UI: https://stokflow-api-0odr.onrender.com/docs<br>
ReDoc: https://stokflow-api-0odr.onrender.com/redoc<br>
API: https://stokflow-api-0odr.onrender.com<br>


Production Infrastructure
Component	       |    Service
API	                  Render
Database	        Neon PostgreSQL
Redis	               Upstash Redis
Containerization	    Docker
CI/CD	              GitHub Actions
API Documentation	  Swagger / OpenAPI

The production API runs on a Render Free Web Service.

PostgreSQL is hosted on Neon, while Redis is provided by Upstash.

<img width="1916" height="980" alt="Screenshot 2026-08-08 040500" src="https://github.com/user-attachments/assets/5cc1f6cc-6f6a-483c-bd88-c04152592b17" />




☁️ Production Deployment

The API is deployed using the following architecture:

                     Internet
                        │
                        ▼
              ┌──────────────────┐
              │      Render      │
              │   FastAPI API    │
              │     Docker       │
              └────────┬─────────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
     ┌────────────────┐  ┌────────────────┐
     │ Neon PostgreSQL│  │ Upstash Redis  │
     │                │  │                │
     │ Production DB  │  │ Cache / Celery │
     └────────────────┘  │ infrastructure │


Production services

Render

Hosts the Dockerized FastAPI application.

Neon

Provides the production PostgreSQL database.

Upstash

Provides the production Redis instance used by the application and Celery configuration.

GitHub Actions

Runs automated tests and code-quality checks.


## Features 🚀


### Authentication & Authorization
* JWT-based user authentication
* Refresh token authentication with token rotation support
* Secure refresh token storage and validation
* Refresh token expiration and revocation handling
* Secure password hashing with bcrypt
* Email verification system with verification links
* Role-based authorization (Admin/User)
* Protected user-specific resources
* Authentication rate limiting to prevent brute-force login attempts
* Admin management capabilities
* Admin user management

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

  <img width="1917" height="1057" alt="Screenshot 2026-08-03 220222" src="https://github.com/user-attachments/assets/7d380b26-9e05-40a2-b7df-3f7348091688" />


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

<img width="1912" height="972" alt="Screenshot 2026-08-02 200041" src="https://github.com/user-attachments/assets/e786196f-63ed-476f-938e-a0b0ef56ca71" />
<img width="1912" height="971" alt="Screenshot 2026-08-02 200059" src="https://github.com/user-attachments/assets/bc28ada7-17e0-46a9-92bc-090a70e3e33e" />

### Background Tasks & Async Processing
* Background Tasks & Async Processing
* Celery integration for asynchronous background jobs
* Redis used as Celery message broker and result backend
* Asynchronous email delivery without blocking API requests
* Background email verification task processing
* Improved API responsiveness by moving long-running tasks to workers
* Scalable worker-based task execution architecture
<img width="1872" height="991" alt="Screenshot 2026-08-03 015904" src="https://github.com/user-attachments/assets/c72032f9-e4a4-42dc-a764-609bd77b7959" />
<img width="1902" height="1040" alt="Screenshot 2026-08-03 015759" src="https://github.com/user-attachments/assets/3cc27cc3-60a9-4c8a-b460-5385a36e4bc8" />

The application integrates Celery for asynchronous background processing.

Redis is used as:

Celery message broker
Celery result backend

Background tasks include operations such as asynchronous email processing and email verification.
This prevents long-running operations from blocking API requests and provides a worker-based architecture that can be scaled independently.

Celery is fully integrated into the application and Docker development environment. The current production deployment uses the Render Free Web Service; a separate paid Render Background Worker is not required for the current deployment.


## Caching & Performance
- Redis integration for API response caching
- Async Redis operations for improved performance
- Cache management with configurable expiration times (TTL)
- Cached frequently accessed resources (Products, Users, Categories, Stock Movements)
- Automatic cache invalidation support for data updates
- Redis is provided in production by Upstash Redis.

<img width="1918" height="1056" alt="Screenshot 2026-08-02 175031" src="https://github.com/user-attachments/assets/e005248b-de76-433c-98f4-79c7ed31e28c" />
<img width="1893" height="1047" alt="Screenshot 2026-08-02 181926" src="https://github.com/user-attachments/assets/918060d1-7b0e-4c99-8d34-1834368e9576" />


📊 Monitoring & Observability

StockFlow exposes application and infrastructure metrics using Prometheus and provides a monitoring dashboard through Grafana.

Prometheus collects metrics from the FastAPI /metrics endpoint, while Grafana is used to visualize application performance and business metrics.

Monitored Metrics
* HTTP request rate and request counts
* HTTP request latency
* Process and memory metrics
* Cache hit and miss rates
* Stock movement metrics (IN / OUT)
* Python runtime and garbage collection metrics
* Monitoring Architecture

FastAPI
   │
   │ /metrics
   ▼
Prometheus
   │
   │ PromQL
   ▼
Grafana Dashboard

Prometheus and Grafana are included in the Docker Compose development environment.

Prometheus scrapes the API metrics every 15 seconds, while Grafana provides dashboards for monitoring API performance, caching behavior and inventory activity.



### API Documentation & Quality
* Swagger/OpenAPI interactive documentation
* Automated testing with Pytest for authentication and category features
* Code quality improvements with Ruff linting and formatting

### API Quality & CI/CD
* Automated testing with Pytest
* CI pipeline for automated checks
* Code quality checks with Ruff
* Swagger/OpenAPI documentation

### Testing Strategy 🧪
* API integration testing with Pytest
* Integration tests for authentication and category features
* Test database isolation using a separate test database
* Mocked Celery background tasks
* Automated test execution with GitHub Actions CI
<img width="1895" height="1032" alt="Screenshot 2026-07-31 210242" src="https://github.com/user-attachments/assets/b09d6660-4d64-453c-9caf-6b5a92bce514" />

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
* Refresh token authentication
* Secure refresh token storage and validation
* Refresh token expiration and revocation handling
* bcrypt (Password hashing)
* Role-Based Access Control (RBAC)
* Authentication rate limiting
* Protected API routes

<img width="1917" height="982" alt="Screenshot 2026-08-07 222039" src="https://github.com/user-attachments/assets/c9c7dffb-5417-4013-b60c-7df97e1831f7" />
<img width="1917" height="1013" alt="Screenshot 2026-08-07 222131" src="https://github.com/user-attachments/assets/a007a3b7-678d-4a88-a9a5-db2897e69fa4" />
<img width="1917" height="996" alt="Screenshot 2026-08-07 222354" src="https://github.com/user-attachments/assets/9d5a4324-a94b-4e8f-b71b-a9d738d87c4b" />


### Architecture & Development
* Service Layer Architecture
* Repository Pattern
* Dependency Injection (FastAPI Dependencies)
* Custom Exception Handling

### File & Email Services
* File upload handling
* Image validation and management
* Email verification system

🧪 Testing

Testing is implemented with Pytest.

The test suite covers areas including:

* Authentication
* Users
* Products
* Categories
* Stock movements

Testing also includes:

* API integration tests
* Test database isolation
* Mocked background tasks
* Authentication scenarios
* Authorization scenarios

Run tests locally:

pytest

🧹 Code Quality

The project uses Ruff for linting and formatting.

Check code:

ruff check .

Check formatting:

ruff format --check .

Format code:

ruff format .

🔄 CI/CD

GitHub Actions is used for automated quality checks.

The CI pipeline performs automated checks such as:

Push / Pull Request
       │
       ▼
GitHub Actions
       │
       ├── Pytest
       │
       └── Ruff

This ensures that tests and code-quality checks are executed automatically before changes are considered complete.

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
- redis

🐳 Docker

The application includes a Dockerfile for containerized deployment.

Example:

FROM python:3.14

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Docker Compose is used for local development and can orchestrate the application and supporting services.


🧩 Design Patterns

The project uses several backend design practices:

Router Layer

Responsible for:

* HTTP requests
* HTTP responses
* Dependency injection
* Endpoint definitions
* Service Layer

Responsible for:

* Business logic
* Authentication
* Authorization
* Inventory rules
* Cache handling
* Background task coordination
* Repository Layer

Responsible for:

* Database access
* CRUD operations
* Query execution

Repositories do not contain business logic.


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

## 🚀 Future Improvements

1. Expand automated test coverage <br>
2. Add more comprehensive integration tests<br>
3. Add database indexes based on production query analysis<br>
4. Add monitoring and application metrics<br>
5. Add production Celery worker deployment<br>
6. Add a frontend application<br>
7. Add advanced inventory reporting<br>
8. Improve observability and distributed logging<br>
9. Add automated production deployment workflows<br>
---

# 👨‍💻 Author

**Irhad Kunovac**

GitHub:
https://github.com/irhadTTT

---

# 📄 License
This project is licensed under the MIT License.
