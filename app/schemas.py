from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=4)

class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Product name cannot be empty")
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than zero")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
