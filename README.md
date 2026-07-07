# FastAPI Products CRUD API

This project is a RESTful API built with **FastAPI** for managing products. It supports full CRUD operations and uses **SQLite** as the database with **SQLAlchemy** for ORM mapping. Input validation is handled automatically via **Pydantic**.

## Tech Stack
- **Python 3.12+**
- **FastAPI** (Web Framework)
- **SQLite** (Database)
- **SQLAlchemy ORM** (Object-Relational Mapping)
- **Pydantic** (Data Validation)
- **Uvicorn** (ASGI Server)

## Folder Structure
```
app/
│── __init__.py
│── main.py       # FastAPI application and route definitions
│── database.py   # SQLAlchemy setup and connection
│── models.py     # SQLAlchemy models (Database schema)
│── schemas.py    # Pydantic schemas (Data validation)
│── crud.py       # CRUD operations (Business logic)
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
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

## How to Run

Start the FastAPI development server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be running at `http://127.0.0.1:8000`.

## Swagger URL

You can access the interactive API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

### 1. Create a Product
- **Method:** `POST /items`
- **Description:** Creates a new product.
- **Validation Rules:**
  - `name`: Cannot be empty (min length 1).
  - `price`: Must be strictly greater than zero.
  - `description`: Optional string.

**Example Request (JSON):**
```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse",
  "price": 29.99
}
```

**Example Response (201 Created):**
```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse",
  "price": 29.99,
  "id": 1
}
```

### 2. Get All Products
- **Method:** `GET /items`
- **Description:** Returns a list of products.
- **Query Parameters:**
  - `skip` (default=0): For pagination.
  - `limit` (default=100): Maximum records to return.

**Example Response (200 OK):**
```json
[
  {
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": 29.99,
    "id": 1
  }
]
```

### 3. Get Product by ID
- **Method:** `GET /items/{id}`
- **Description:** Returns a single product matching the given ID.
- **Example Response (200 OK):** *(same as create response)*
- **Error Response (404 Not Found):**
  ```json
  {
    "detail": "Product not found"
  }
  ```

### 4. Update Product
- **Method:** `PUT /items/{id}`
- **Description:** Updates an existing product.
- **Example Request (JSON):**
  ```json
  {
    "name": "Advanced Wireless Mouse",
    "price": 35.99
  }
  ```
- **Example Response (200 OK):**
  ```json
  {
    "name": "Advanced Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "price": 35.99,
    "id": 1
  }
  ```

### 5. Delete Product
- **Method:** `DELETE /items/{id}`
- **Description:** Deletes a product.
- **Example Response (200 OK):**
  ```json
  {
    "detail": "Product deleted"
  }
  ```

## Postman Instructions

A Postman collection is included in this repository: `postman_collection.json`.

**To use the collection:**
1. Open Postman.
2. Click **Import** > **File** > select `postman_collection.json`.
3. The collection is configured to use an environment variable `base_url` set to `http://127.0.0.1:8000`.
4. Ensure the server is running.
5. Run the requests sequentially, or use the **Collection Runner** to execute all tests automatically. The "Create Product" test will capture the `product_id` to test subsequent endpoints properly.

## Assumptions
- Product names do not need to be strictly unique across the database, though they are indexed for fast searching.
- The `skip` and `limit` pagination is offset-based, which is standard for simple CRUD APIs.
- For updating, any omitted field will not overwrite existing fields, only explicitly provided fields are updated.
