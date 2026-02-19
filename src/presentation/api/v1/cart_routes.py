from fastapi import APIRouter, Depends, HTTPException, status
from src.presentation.api.schemas.cart_schema import CartCheckoutResult, CartCreate, CartItemInput, CartRead
from src.application.dto.model.cart_schema import CartCreate as CartCreateDto, CartItemInput as CartItemInputDto
from src.application.interface.service.cart_service import ICartService
from src.infrastructure.ioc.service import get_cart_service

router = APIRouter()


@router.post("/", response_model=CartRead)
async def create(data: CartCreate, service: ICartService = Depends(get_cart_service)):
    cart = await service.create(CartCreateDto(**data.model_dump()))
    return CartRead.model_validate(cart)


@router.get("/{cart_id}", response_model=CartRead)
async def get(cart_id: int, service: ICartService = Depends(get_cart_service)):
    cart = await service.get(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return CartRead.model_validate(cart)


@router.post("/{cart_id}/items", response_model=CartRead)
async def add_item(cart_id: int, data: CartItemInput, service: ICartService = Depends(get_cart_service)):
    try:
        cart = await service.add_item(cart_id, CartItemInputDto(**data.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return CartRead.model_validate(cart)


@router.post("/{cart_id}/checkout", response_model=CartCheckoutResult)
async def checkout(cart_id: int, service: ICartService = Depends(get_cart_service)):
    try:
        result = await service.checkout(cart_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return CartCheckoutResult.model_validate(result)
