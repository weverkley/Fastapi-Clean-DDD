from datetime import datetime
from .base import BaseEntity


class ProcessedMessageEntity(BaseEntity):
    consumer_name: str
    message_id: str
    processed_at: datetime
