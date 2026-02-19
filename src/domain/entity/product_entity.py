from decimal import Decimal
from .base import BaseEntity


class ProductEntity(BaseEntity):
    name: str
    sku: str
    price: Decimal
    active: bool
