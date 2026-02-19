from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.product_entity import ProductEntity
from src.domain.interface.repository.product_repository import IProductRepository
from src.infrastructure.data.repository.base import BaseRepository


class ProductRepository(BaseRepository[ProductEntity], IProductRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductEntity)

    async def get_by_sku(self, sku: str) -> ProductEntity | None:
        stmt = select(self.model).where(self.model.sku == sku)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
