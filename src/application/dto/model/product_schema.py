from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    sku: str
    price: Decimal
    active: bool = True


class ProductRead(ProductBase):
    id: int | None = None

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[Decimal] = None
    active: Optional[bool] = None
