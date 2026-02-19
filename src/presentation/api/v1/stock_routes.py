from fastapi import APIRouter, Depends, HTTPException, status
from src.presentation.api.schemas.stock_schema import StockAdjust, StockCreate, StockRead
from src.application.dto.model.stock_schema import StockCreate as StockCreateDto
from src.application.interface.service.stock_service import IStockService
from src.infrastructure.ioc.service import get_stock_service

router = APIRouter()


@router.post("/", response_model=StockRead)
async def create(data: StockCreate, service: IStockService = Depends(get_stock_service)):
    stock = await service.create(StockCreateDto(**data.model_dump()))
    return StockRead.model_validate(stock)


@router.get("/{product_id}", response_model=StockRead)
async def get_by_product(product_id: int, service: IStockService = Depends(get_stock_service)):
    stock = await service.get_by_product_id(product_id)
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return StockRead.model_validate(stock)


@router.post("/{product_id}/adjust", response_model=StockRead)
async def adjust(product_id: int, data: StockAdjust, service: IStockService = Depends(get_stock_service)):
    try:
        stock = await service.adjust(product_id, data.quantity_delta)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return StockRead.model_validate(stock)
