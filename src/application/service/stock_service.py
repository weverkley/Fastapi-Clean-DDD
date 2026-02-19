from src.application.dto.model.stock_schema import StockCreate, StockRead, StockUpdate
from src.application.interface.service.stock_service import IStockService
from src.application.service.base import BaseService
from src.domain.entity.stock_entity import StockEntity
from src.domain.interface.repository.stock_repository import IStockRepository


class StockService(BaseService[StockRead, StockCreate, StockUpdate], IStockService):
    def __init__(self, repo: IStockRepository):
        super().__init__(repo, StockEntity, StockRead)
        self._repo = repo

    async def get_by_product_id(self, product_id: int) -> StockRead | None:
        stock = await self._repo.get_by_product_id(product_id)
        if not stock:
            return None
        return StockRead.model_validate(stock)

    async def create(self, data: StockCreate) -> StockRead:
        existing = await self._repo.get_by_product_id(data.product_id)
        if existing:
            return StockRead.model_validate(existing)
        return await super().create(data)

    async def adjust(self, product_id: int, quantity_delta: int) -> StockRead | None:
        current = await self._repo.get_by_product_id(product_id)
        if not current:
            return None

        stock = await self._repo.adjust_available(product_id, quantity_delta)
        if not stock:
            raise ValueError("Stock adjustment would result in negative availability.")
        await self._repo.session.commit()  # type: ignore[attr-defined]
        return StockRead.model_validate(stock)
