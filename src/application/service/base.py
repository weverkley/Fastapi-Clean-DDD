from pydantic import BaseModel
from typing import TypeVar, Type, Sequence
from src.application.interface.service.base_service import IBaseService
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.base import BaseEntity
from src.infrastructure.data.repository.base import BaseRepository
from automapper import mapper

ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
EntityType = TypeVar("EntityType", bound=BaseEntity)
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(IBaseService[ReadSchema, CreateSchema, UpdateSchema]):
    def __init__(self, repo: IBaseRepository[EntityType], entity: Type[EntityType], read_schema: Type[ReadSchema]):
        self._repo = repo
        self._entity = entity
        self._read_schema = read_schema

    async def list(self) -> Sequence[ReadSchema]:
        items = await self._repo.list()
        return [self._read_schema.model_validate(item) for item in items]

    async def get(self, id: int) -> ReadSchema | None:
        item = await self._repo.get(id)
        if item:
            return self._read_schema.model_validate(item)
        return None
        
    async def create(self, data: CreateSchema) -> ReadSchema:
        entity = mapper.to(self._entity).map(data)
        created = await self._repo.create(entity)
        return self._read_schema.model_validate(created)
        
    async def update(self, id: int, data: UpdateSchema) -> ReadSchema | None:
        updated = await self._repo.update(id, data.model_dump(exclude_unset=True))
        if updated:
            return self._read_schema.model_validate(updated)
        return None

    async def delete(self, id: int) -> None:
        await self._repo.delete(id)