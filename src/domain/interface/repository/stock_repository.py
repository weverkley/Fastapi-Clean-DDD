from abc import ABC, abstractmethod
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.stock_entity import StockEntity


class IStockRepository(IBaseRepository[StockEntity], ABC):
    @abstractmethod
    async def get_by_product_id(self, product_id: int) -> StockEntity | None: ...

    @abstractmethod
    async def reserve(self, product_id: int, quantity: int) -> bool: ...

    @abstractmethod
    async def mark_sold(self, product_id: int, quantity: int) -> None: ...

    @abstractmethod
    async def adjust_available(self, product_id: int, quantity_delta: int) -> StockEntity | None: ...
