from abc import ABC, abstractmethod


class IProcessedMessageStore(ABC):
    @abstractmethod
    async def exists(self, consumer_name: str, message_id: str) -> bool: ...

    @abstractmethod
    async def add(self, consumer_name: str, message_id: str) -> None: ...
