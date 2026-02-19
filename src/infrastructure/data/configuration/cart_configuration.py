from sqlalchemy import Table, Column, Integer, ForeignKey, String, Numeric, DateTime, text
from sqlalchemy.orm import registry
from src.domain.entity.cart_entity import CartEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

CartConfiguration = Table(
    "carts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("status", String(30), nullable=False, server_default=text("'open'")),
    Column("total_amount", Numeric(12, 2), nullable=False, server_default=text("0")),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)


def map_cart() -> None:
    mapper_registry.map_imperatively(CartEntity, CartConfiguration)
