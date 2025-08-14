from typing import Generic, TypeVar, Sequence
from abc import ABC, abstractmethod

from pydantic import BaseModel

ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)

class IBaseService(Generic[ReadSchema, CreateSchema, UpdateSchema], ABC):
    @abstractmethod
    async def list(self) -> Sequence[ReadSchema]: ...
    
    @abstractmethod
    async def get(self, id: int) -> ReadSchema | None: ...

    @abstractmethod
    async def create(self, data: CreateSchema) -> ReadSchema: ...

    @abstractmethod
    async def update(self, id: int, data: UpdateSchema) -> ReadSchema | None: ...

    @abstractmethod
    async def delete(self, id: int) -> None: ...