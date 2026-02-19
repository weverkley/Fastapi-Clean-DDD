from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.interface.service.order_service import IOrderService
from src.infrastructure.ioc.service import get_order_service
from src.presentation.api.schemas.order_schema import OrderRead

router = APIRouter()


@router.get("/", response_model=List[OrderRead])
async def list_orders(service: IOrderService = Depends(get_order_service)):
    orders = await service.list()
    return [OrderRead.model_validate(order) for order in orders]


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, service: IOrderService = Depends(get_order_service)):
    order = await service.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return OrderRead.model_validate(order)
