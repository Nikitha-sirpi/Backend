from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

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

    model_config = ConfigDict(from_attributes=True)
