from decimal import Decimal
from pydantic import BaseModel


class CartItemInput(BaseModel):
    product_id: int
    quantity: int


class CartItemRead(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True


class CartCreate(BaseModel):
    user_id: int


class CartRead(BaseModel):
    id: int
    user_id: int
    status: str
    total_amount: Decimal
    items: list[CartItemRead] = []

    class Config:
        from_attributes = True


class CartCheckoutResult(BaseModel):
    cart_id: int
    status: str
    event_id: str
