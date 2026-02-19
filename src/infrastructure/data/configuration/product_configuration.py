from sqlalchemy import Table, Column, Integer, String, Numeric, Boolean, UniqueConstraint, text
from sqlalchemy.orm import registry
from src.domain.entity.product_entity import ProductEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

ProductConfiguration = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("sku", String(80), nullable=False),
    Column("price", Numeric(12, 2), nullable=False),
    Column("active", Boolean, nullable=False, server_default=text("true")),
    UniqueConstraint("sku", name="uq_products_sku"),
)


def map_product() -> None:
    mapper_registry.map_imperatively(ProductEntity, ProductConfiguration)
