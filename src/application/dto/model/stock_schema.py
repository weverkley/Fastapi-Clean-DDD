from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    product_id: int
    available_quantity: int
    reserved_quantity: int = 0


class StockRead(StockBase):
    id: int | None = None

    class Config:
        from_attributes = True


class StockCreate(StockBase):
    pass


class StockAdjust(BaseModel):
    quantity_delta: int


class StockUpdate(BaseModel):
    id: int
    available_quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
