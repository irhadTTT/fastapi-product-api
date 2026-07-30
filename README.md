# FastAPI Product API 🚀

REST API built with FastAPI, PostgreSQL, SQLAlchemy, Alembic and Docker.

---

# 📌 Features

- User authentication with JWT
- Role based authorization
- Product CRUD operations
- PostgreSQL database
- Database migrations with Alembic
- Dockerized development environment
- Swagger API documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker
- JWT

## Installation

### Clone repository

git clone ...

### Start services

docker compose up --build

## Environment Variables

DATABASE_URL=
SECRET_KEY=
ALGORITHM=

## Database migrations

alembic upgrade head

## API Documentation

Open:

http://localhost:8000/docs

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

## Admin account (development)

For testing admin endpoints, use the default admin account:

Username: admin
Password: admin123


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

        ┌───────────────┐
        │   FastAPI     │
        │    Routes     │
        └───────┬───────┘
                |
                ▼

        ┌───────────────┐
        │   Schemas     │
        │   Pydantic    │
        └───────┬───────┘
                |
                ▼

        ┌───────────────┐
        │ SQLAlchemy    │
        │    Models     │
        └───────┬───────┘
                |
                ▼

        ┌───────────────┐
        │    SQLite     │
        │   Database    │
        └───────────────┘
```

---

# 📂 Project Structure

```text
fastapi-product-api/

│
├── app/
│   │
│   ├── main.py              # Application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── auth.py               # Authentication logic
│   │
│   ├── routers/
│   │   ├── products.py       # Product endpoints
│   │   └── users.py          # User endpoints
│   │
│   └── dependencies.py       # API dependencies
│
├── requirements.txt
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

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./database.sqlite3
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# ▶️ Run Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

Application runs at:

```text
http://127.0.0.1:8000
```

---

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
