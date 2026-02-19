from abc import ABC, abstractmethod
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.product_entity import ProductEntity


class IProductRepository(IBaseRepository[ProductEntity], ABC):
    @abstractmethod
    async def get_by_sku(self, sku: str) -> ProductEntity | None: ...
