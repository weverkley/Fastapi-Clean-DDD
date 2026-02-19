from typing import Sequence
from src.application.dto.model.order_schema import OrderRead
from src.application.interface.service.order_service import IOrderService
from src.domain.interface.repository.order_repository import IOrderRepository


class OrderService(IOrderService):
    def __init__(self, repo: IOrderRepository):
        self._repo = repo

    async def list(self) -> Sequence[OrderRead]:
        orders = await self._repo.list()
        return [OrderRead.model_validate(order) for order in orders]

    async def get(self, id: int) -> OrderRead | None:
        order = await self._repo.get(id)
        if not order:
            return None
        return OrderRead.model_validate(order)
