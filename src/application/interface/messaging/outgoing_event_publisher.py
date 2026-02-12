from abc import ABC, abstractmethod
from src.application.dto.messaging.outgoing_event import OutgoingEvent


class IOutgoingEventPublisher(ABC):
    async def start(self) -> None:
        return None

    async def close(self) -> None:
        return None

    @abstractmethod
    async def publish(self, event: OutgoingEvent) -> None: ...
