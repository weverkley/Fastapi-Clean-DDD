from src.application.dto.model.product_schema import ProductCreate, ProductRead, ProductUpdate
from src.application.interface.service.product_service import IProductService
from src.application.service.base import BaseService
from src.domain.entity.product_entity import ProductEntity
from src.domain.interface.repository.product_repository import IProductRepository


class ProductService(BaseService[ProductRead, ProductCreate, ProductUpdate], IProductService):
    def __init__(self, repo: IProductRepository):
        super().__init__(repo, ProductEntity, ProductRead)
