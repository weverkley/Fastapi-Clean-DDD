from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import registry
from src.domain.entity.stock_entity import StockEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

StockConfiguration = Table(
    "stocks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
    Column("available_quantity", Integer, nullable=False, server_default=text("0")),
    Column("reserved_quantity", Integer, nullable=False, server_default=text("0")),
    UniqueConstraint("product_id", name="uq_stocks_product_id"),
    CheckConstraint("available_quantity >= 0", name="ck_stocks_available_non_negative"),
    CheckConstraint("reserved_quantity >= 0", name="ck_stocks_reserved_non_negative"),
)


def map_stock() -> None:
    mapper_registry.map_imperatively(StockEntity, StockConfiguration)
