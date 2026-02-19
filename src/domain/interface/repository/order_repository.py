from abc import ABC, abstractmethod
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.order_entity import OrderEntity


class IOrderRepository(IBaseRepository[OrderEntity], ABC):
    @abstractmethod
    async def get_by_cart_id(self, cart_id: int) -> OrderEntity | None: ...

    @abstractmethod
    async def set_status(self, order_id: int, status: str) -> None: ...
