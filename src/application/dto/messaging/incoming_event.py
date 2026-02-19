from dataclasses import dataclass
from collections.abc import Callable


@dataclass
class IncomingEvent:
    message_id: str
    idempotency_key: str
    payload: str
    source: str
    event_type: str | None = None
    correlation_id: str | None = None
    ack: Callable[[], object] | None = None
    nack: Callable[[], object] | None = None
