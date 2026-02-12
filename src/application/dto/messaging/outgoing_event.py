from dataclasses import dataclass


@dataclass
class OutgoingEvent:
    event_id: str
    event_type: str
    event_version: int
    exchange: str
    routing_key: str
    payload: str
    correlation_id: str | None = None
