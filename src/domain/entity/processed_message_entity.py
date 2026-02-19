from datetime import datetime
from .base import BaseEntity


class ProcessedMessageEntity(BaseEntity):
    consumer_name: str
    message_id: str
    status: str
    first_seen_at: datetime
    processed_at: datetime | None
    last_error: str | None
    attempt_count: int
