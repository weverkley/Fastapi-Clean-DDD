from abc import abstractmethod
from src.application.interface.service.base_service import IBaseService
from src.application.dto.model.stock_schema import StockCreate, StockRead, StockUpdate


class IStockService(IBaseService[StockRead, StockCreate, StockUpdate]):
    @abstractmethod
    async def get_by_product_id(self, product_id: int) -> StockRead | None: ...

    @abstractmethod
    async def adjust(self, product_id: int, quantity_delta: int) -> StockRead | None: ...
