from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.presentation.api.schemas.product_schema import ProductCreate, ProductRead, ProductUpdate
from src.application.dto.model.product_schema import ProductCreate as ProductCreateDto, ProductUpdate as ProductUpdateDto
from src.application.interface.service.product_service import IProductService
from src.infrastructure.ioc.service import get_product_service

router = APIRouter()


@router.post("/", response_model=ProductRead)
async def create(data: ProductCreate, service: IProductService = Depends(get_product_service)):
    product = await service.create(ProductCreateDto(**data.model_dump()))
    return ProductRead.model_validate(product)


@router.get("/{id}", response_model=ProductRead)
async def get(id: int, service: IProductService = Depends(get_product_service)):
    product = await service.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductRead.model_validate(product)


@router.get("/", response_model=List[ProductRead])
async def list(service: IProductService = Depends(get_product_service)):
    products = await service.list()
    return [ProductRead.model_validate(product) for product in products]


@router.put("/{id}", response_model=ProductRead)
async def update(id: int, data: ProductUpdate, service: IProductService = Depends(get_product_service)):
    product = await service.update(id, ProductUpdateDto(**data.model_dump()))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductRead.model_validate(product)


@router.delete("/{id}")
async def delete(id: int, service: IProductService = Depends(get_product_service)):
    await service.delete(id)
    return {"status": "deleted"}
