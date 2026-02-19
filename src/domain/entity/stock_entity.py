from .base import BaseEntity


class StockEntity(BaseEntity):
    product_id: int
    available_quantity: int
    reserved_quantity: int
