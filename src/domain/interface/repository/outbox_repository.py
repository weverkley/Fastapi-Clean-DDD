from abc import ABC, abstractmethod
from src.domain.entity.outbox_message_entity import OutboxMessageEntity


class IOutboxRepository(ABC):
    @abstractmethod
    async def add(self, message: OutboxMessageEntity) -> None: ...

    @abstractmethod
    async def claim_pending(self, limit: int) -> list[OutboxMessageEntity]: ...

    @abstractmethod
    async def mark_published(self, message_id: int) -> None: ...

    @abstractmethod
    async def mark_failed(self, message_id: int, error: str, max_attempts: int) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...
