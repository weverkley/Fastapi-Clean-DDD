from abc import ABC, abstractmethod
from typing import Sequence
from src.application.dto.model.order_schema import OrderRead


class IOrderService(ABC):
    @abstractmethod
    async def list(self) -> Sequence[OrderRead]: ...

    @abstractmethod
    async def get(self, id: int) -> OrderRead | None: ...
