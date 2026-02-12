from dataclasses import dataclass
from typing import Callable


@dataclass
class IncomingEvent:
    message_id: str
    payload: str
    source: str
    event_type: str | None = None
    correlation_id: str | None = None
    ack: Callable[[], None] | None = None
    nack: Callable[[], None] | None = None
