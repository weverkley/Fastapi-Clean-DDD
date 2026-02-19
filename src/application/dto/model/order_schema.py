from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class OrderRead(BaseModel):
    id: int
    cart_id: int
    user_id: int
    status: str
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
