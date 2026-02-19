from sqlalchemy import Table, Column, Integer, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import registry
from src.domain.entity.cart_item_entity import CartItemEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

CartItemConfiguration = Table(
    "cart_items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cart_id", Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id", ondelete="RESTRICT"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Numeric(12, 2), nullable=False),
    CheckConstraint("quantity > 0", name="ck_cart_items_quantity_positive"),
)


def map_cart_item() -> None:
    mapper_registry.map_imperatively(CartItemEntity, CartItemConfiguration)
