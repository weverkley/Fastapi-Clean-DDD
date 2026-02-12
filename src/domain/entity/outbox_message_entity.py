from datetime import datetime
from .base import BaseEntity


class OutboxMessageEntity(BaseEntity):
    event_id: str
    event_type: str
    event_version: int
    exchange: str
    routing_key: str
    payload: str
    correlation_id: str | None
    status: str
    attempts: int
    available_at: datetime
    published_at: datetime | None
    last_error: str | None
    created_at: datetime
    updated_at: datetime
