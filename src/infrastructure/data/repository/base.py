from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Sequence, TypeVar, Generic, Type
from src.domain.entity.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def get(self, id: int) -> T | None:
        return await self.session.get(self.model, id)

    async def list(self) -> Sequence[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, obj_data: dict) -> T | None:
        obj = await self.get(id)
        if obj:
            for key, value in obj_data.items():
                setattr(obj, key, value)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
        return obj

    async def delete(self, id: int) -> None:
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()