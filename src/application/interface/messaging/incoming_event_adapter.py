from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from src.application.dto.messaging.incoming_event import IncomingEvent


class IIncomingEventAdapter(ABC):
    @abstractmethod
    async def consume(self, on_event: Callable[[IncomingEvent], Awaitable[None]]) -> None: ...
