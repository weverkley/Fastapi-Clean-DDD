from sqlalchemy import DateTime, Integer, Table, Column, String, Text, text
from sqlalchemy.orm import registry
from src.domain.entity.outbox_message_entity import OutboxMessageEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

OutboxMessageConfiguration = Table(
    "outbox_messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("event_id", String(64), nullable=False, unique=True),
    Column("event_type", String(120), nullable=False),
    Column("event_version", Integer, nullable=False, server_default=text("1")),
    Column("exchange", String(120), nullable=False),
    Column("routing_key", String(120), nullable=False),
    Column("payload", Text, nullable=False),
    Column("correlation_id", String(64), nullable=True),
    Column("status", String(20), nullable=False, server_default=text("'pending'")),
    Column("attempts", Integer, nullable=False, server_default=text("0")),
    Column("available_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("published_at", DateTime(timezone=True), nullable=True),
    Column("dead_lettered_at", DateTime(timezone=True), nullable=True),
    Column("last_error", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column("updated_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)


def map_outbox_message():
    mapper_registry.map_imperatively(OutboxMessageEntity, OutboxMessageConfiguration)
