from sqlalchemy import Table, Column, Integer, ForeignKey, String, Numeric, DateTime, UniqueConstraint, text
from sqlalchemy.orm import registry
from src.domain.entity.order_entity import OrderEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

OrderConfiguration = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("cart_id", Integer, ForeignKey("carts.id", ondelete="RESTRICT"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
    Column("status", String(30), nullable=False, server_default=text("'created'")),
    Column("total_amount", Numeric(12, 2), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    UniqueConstraint("cart_id", name="uq_orders_cart_id"),
)


def map_order() -> None:
    mapper_registry.map_imperatively(OrderEntity, OrderConfiguration)
