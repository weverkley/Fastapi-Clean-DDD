from decimal import Decimal
from datetime import datetime
from .base import BaseEntity


class CartEntity(BaseEntity):
    user_id: int
    status: str
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
