from abc import ABC, abstractmethod


class IEventBus(ABC):
    @abstractmethod
    async def publish(
        self,
        *,
        exchange: str,
        routing_key: str,
        payload: str,
        event_id: str,
        event_type: str,
        event_version: int,
        correlation_id: str | None = None,
    ) -> None: ...
