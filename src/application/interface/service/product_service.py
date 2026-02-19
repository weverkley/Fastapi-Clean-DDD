from src.application.interface.service.base_service import IBaseService
from src.application.dto.model.product_schema import ProductCreate, ProductRead, ProductUpdate


class IProductService(IBaseService[ProductRead, ProductCreate, ProductUpdate]):
    pass
