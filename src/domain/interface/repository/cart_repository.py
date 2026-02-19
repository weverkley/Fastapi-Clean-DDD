from abc import ABC, abstractmethod
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.cart_entity import CartEntity
from src.domain.entity.cart_item_entity import CartItemEntity


class ICartRepository(IBaseRepository[CartEntity], ABC):
    @abstractmethod
    async def list_items(self, cart_id: int) -> list[CartItemEntity]: ...

    @abstractmethod
    async def add_item(self, cart_id: int, product_id: int, quantity: int, unit_price: float) -> None: ...

    @abstractmethod
    async def set_status(self, cart_id: int, status: str, total_amount: float | None = None) -> None: ...

    @abstractmethod
    async def recalculate_total(self, cart_id: int): ...
