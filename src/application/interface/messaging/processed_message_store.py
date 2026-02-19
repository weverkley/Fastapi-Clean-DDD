from abc import ABC, abstractmethod


class IProcessedMessageStore(ABC):
    @abstractmethod
    async def try_begin_processing(self, consumer_name: str, message_id: str) -> bool: ...

    @abstractmethod
    async def mark_processed(self, consumer_name: str, message_id: str) -> None: ...

    @abstractmethod
    async def mark_failed(self, consumer_name: str, message_id: str, error: str) -> None: ...
