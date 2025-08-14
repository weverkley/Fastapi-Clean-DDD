from typing import Generic, TypeVar, Sequence
from abc import ABC, abstractmethod
from src.domain.entity.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)

class IBaseRepository(Generic[T], ABC):
    @abstractmethod
    async def list(self) -> Sequence[T]: ...
    
    @abstractmethod
    async def get(self, id: int) -> T | None: ...

    @abstractmethod
    async def create(self, obj: T) -> T: ...

    @abstractmethod
    async def update(self, id: int, obj_data: dict) -> T | None: ...

    @abstractmethod
    async def delete(self, id: int) -> None: ...