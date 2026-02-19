from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.stock_entity import StockEntity
from src.domain.interface.repository.stock_repository import IStockRepository
from src.infrastructure.data.repository.base import BaseRepository


class StockRepository(BaseRepository[StockEntity], IStockRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StockEntity)

    async def get_by_product_id(self, product_id: int) -> StockEntity | None:
        stmt = select(self.model).where(self.model.product_id == product_id)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def reserve(self, product_id: int, quantity: int) -> bool:
        stmt = (
            update(self.model)
            .where(self.model.product_id == product_id)  # type: ignore[attr-defined]
            .where(self.model.available_quantity >= quantity)  # type: ignore[attr-defined]
            .values(
                available_quantity=self.model.available_quantity - quantity,  # type: ignore[attr-defined]
                reserved_quantity=self.model.reserved_quantity + quantity,  # type: ignore[attr-defined]
            )
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def mark_sold(self, product_id: int, quantity: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.product_id == product_id)  # type: ignore[attr-defined]
            .where(self.model.reserved_quantity >= quantity)  # type: ignore[attr-defined]
            .values(
                reserved_quantity=self.model.reserved_quantity - quantity,  # type: ignore[attr-defined]
            )
        )
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Insufficient reserved stock for product {product_id}")

    async def adjust_available(self, product_id: int, quantity_delta: int) -> StockEntity | None:
        stmt = (
            update(self.model)
            .where(self.model.product_id == product_id)  # type: ignore[attr-defined]
            .where((self.model.available_quantity + quantity_delta) >= 0)  # type: ignore[attr-defined]
            .values(available_quantity=self.model.available_quantity + quantity_delta)  # type: ignore[attr-defined]
        )
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            return None
        return await self.get_by_product_id(product_id)
