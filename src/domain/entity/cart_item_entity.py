from decimal import Decimal
from .base import BaseEntity


class CartItemEntity(BaseEntity):
    cart_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
