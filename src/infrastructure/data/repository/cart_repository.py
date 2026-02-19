from decimal import Decimal
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.cart_entity import CartEntity
from src.domain.entity.cart_item_entity import CartItemEntity
from src.domain.interface.repository.cart_repository import ICartRepository
from src.infrastructure.data.repository.base import BaseRepository


class CartRepository(BaseRepository[CartEntity], ICartRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CartEntity)

    async def list_items(self, cart_id: int) -> list[CartItemEntity]:
        stmt = select(CartItemEntity).where(CartItemEntity.cart_id == cart_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add_item(self, cart_id: int, product_id: int, quantity: int, unit_price: float) -> None:
        stmt = select(CartItemEntity).where(
            CartItemEntity.cart_id == cart_id,
            CartItemEntity.product_id == product_id,
        )
        result = await self.session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing:
            existing.quantity = existing.quantity + quantity
            self.session.add(existing)
            return

        item = CartItemEntity()
        item.cart_id = cart_id
        item.product_id = product_id
        item.quantity = quantity
        item.unit_price = Decimal(str(unit_price))
        self.session.add(item)

    async def set_status(self, cart_id: int, status: str, total_amount: float | None = None) -> None:
        values: dict[str, object] = {
            "status": status,
            "updated_at": func.now(),
        }
        if total_amount is not None:
            values["total_amount"] = total_amount
        stmt = update(self.model).where(self.model.id == cart_id).values(**values)  # type: ignore[attr-defined]
        await self.session.execute(stmt)

    async def recalculate_total(self, cart_id: int) -> Decimal:
        stmt = select(func.coalesce(func.sum(CartItemEntity.quantity * CartItemEntity.unit_price), 0)).where(
            CartItemEntity.cart_id == cart_id
        )
        result = await self.session.execute(stmt)
        total = result.scalar_one()
        decimal_total = Decimal(str(total))
        await self.session.execute(
            update(self.model)
            .where(self.model.id == cart_id)  # type: ignore[attr-defined]
            .values(total_amount=decimal_total, updated_at=func.now())
        )
        return decimal_total
