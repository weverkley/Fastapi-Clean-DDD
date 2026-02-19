from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.order_entity import OrderEntity
from src.domain.interface.repository.order_repository import IOrderRepository
from src.infrastructure.data.repository.base import BaseRepository


class OrderRepository(BaseRepository[OrderEntity], IOrderRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderEntity)

    async def get_by_cart_id(self, cart_id: int) -> OrderEntity | None:
        stmt = select(self.model).where(self.model.cart_id == cart_id)  # type: ignore[attr-defined]
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def set_status(self, order_id: int, status: str) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == order_id)  # type: ignore[attr-defined]
            .values(status=status, updated_at=func.now())
        )
        await self.session.execute(stmt)
