from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from . import crud, models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Products API with Auth", description="CRUD REST API for Products with JWT Authentication")

# --- Auth Endpoints ---

@app.post("/auth/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- User Endpoints ---

@app.get("/users/me/items", response_model=List[schemas.Product])
def read_my_items(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_products(db, user_id=current_user.id)

# --- Product Endpoints ---

@app.post("/items", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_product(db=db, product=product, user_id=current_user.id)

@app.get("/items", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db),
):
    products = crud.get_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        min_price=min_price,
        max_price=max_price,
    )
    return products

@app.get("/items/{id}", response_model=schemas.Product)
def read_product(id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/items/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = crud.get_product(db, product_id=id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if db_product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to modify this resource.")
        
    return crud.update_product(db=db, product_id=id, product=product)

@app.delete("/items/{id}", status_code=status.HTTP_200_OK)
def delete_product(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_product = crud.get_product(db, product_id=id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
        
    if db_product.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to modify this resource.")
        
    crud.delete_product(db=db, product_id=id)
    return {"detail": "Product deleted"}
