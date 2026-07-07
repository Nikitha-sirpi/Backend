# FastAPI Products CRUD API (Phase 2) - Authentication & Relationships

This project extends the initial RESTful API built with **FastAPI** by adding **User Authentication**, **Relationships**, and **Authorization**. It supports user registration, JWT-based login, and protected product management.

## Tech Stack
- **Python 3.12+**
- **FastAPI** (Web Framework)
- **SQLite** (Database)
- **SQLAlchemy ORM** (Object-Relational Mapping)
- **Pydantic** (Data Validation)
- **Uvicorn** (ASGI Server)
- **Passlib & Bcrypt** (Password Hashing)
- **Python-Jose** (JWT Generation)

## Features (Phase 2 Additions)
- **User Registration & Login**: Users can create an account and authenticate using an email and password.
- **JWT Authentication**: Secure API access via Bearer tokens.
- **One-to-Many Relationship**: Each product is tied to the `user_id` of the user who created it.
- **Protected Routes**: Create, Update, and Delete endpoints require authentication.
- **Resource Authorization**: Only the **owner** of a product can update or delete it (returns `403 Forbidden` otherwise).
- **My Products Endpoint**: Users can fetch only their own products.

## Folder Structure
```
app/
│── __init__.py
│── main.py       # FastAPI application and route definitions
│── database.py   # SQLAlchemy setup and connection
│── models.py     # SQLAlchemy models (User & Product schemas)
│── schemas.py    # Pydantic schemas (Data validation & auth models)
│── crud.py       # CRUD operations (Business logic)
│── auth.py       # Authentication utilities, JWT generation, & hashing
```

## Installation & Setup

1. **Clone or create the project folder**:
   ```bash
   mkdir fastapi_crud
   cd fastapi_crud
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic email-validator
   pip install "passlib[bcrypt]" python-jose[cryptography] python-multipart
   ```

## How to Run

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload
```
The API runs at `http://127.0.0.1:8000`.

## Swagger URL

Interactive API documentation with built-in Authorize button:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Authentication Flow

1. **Register** (`POST /auth/register`): Send an email and password to create an account.
2. **Login** (`POST /auth/login`): Send your email as `username` and your `password`. Receive an `access_token`.
3. **Use Bearer Token**: Include the token in the `Authorization` header for protected routes:
   `Authorization: Bearer <your_access_token>`

## API Endpoints

### Auth Endpoints
- `POST /auth/register`: Create a new user.
- `POST /auth/login`: Authenticate and receive a JWT.

### User Endpoints
- `GET /users/me/items`: (Protected) Return products owned by the currently authenticated user.

### Product Endpoints
- `GET /items`: (Public) Return a paginated list of all products.
- `GET /items/{id}`: (Public) Return a specific product.
- `POST /items`: (Protected) Create a new product. (Automatically assigns `user_id` to current user).
- `PUT /items/{id}`: (Protected & Authorized) Update an existing product. Only the owner can do this.
- `DELETE /items/{id}`: (Protected & Authorized) Delete a product. Only the owner can do this.

## Postman Usage

A Postman collection is included: `postman_collection.json`.

1. Import `postman_collection.json` into Postman.
2. Ensure the server is running.
3. The collection is configured to use the `{{base_url}}` environment variable (set to `http://127.0.0.1:8000`).
4. **Automation**: When you run the `Login` request, a Postman script automatically captures the `access_token` and saves it to the collection variable `{{token}}`. 
5. All protected endpoints are configured to use **Bearer Token** authentication using `{{token}}`. You do not need to manually copy-paste the token!

## Testing

An automated test suite using `pytest` is provided in `test_main.py`.
Run tests via:
```bash
pytest test_main.py
```
This tests Registration, Login, CRUD operations, Relationship assignment, and Authorization (403/401 errors).
