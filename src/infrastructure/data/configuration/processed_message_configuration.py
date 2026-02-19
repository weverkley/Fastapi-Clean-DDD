from sqlalchemy import DateTime, Integer, Table, Column, String, UniqueConstraint, text
from sqlalchemy.orm import registry
from src.domain.entity.processed_message_entity import ProcessedMessageEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

ProcessedMessageConfiguration = Table(
    "processed_messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("consumer_name", String(120), nullable=False),
    Column("message_id", String(128), nullable=False),
    Column("status", String(20), nullable=False, server_default=text("'processing'")),
    Column("first_seen_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("processed_at", DateTime(timezone=True), nullable=True),
    Column("last_error", String(2000), nullable=True),
    Column("attempt_count", Integer, nullable=False, server_default=text("1")),
    UniqueConstraint("consumer_name", "message_id", name="uq_processed_consumer_message"),
)


def map_processed_message():
    mapper_registry.map_imperatively(ProcessedMessageEntity, ProcessedMessageConfiguration)
