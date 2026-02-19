from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interface.repository.user_repository import IUserRepository
from src.domain.interface.repository.product_repository import IProductRepository
from src.domain.interface.repository.stock_repository import IStockRepository
from src.domain.interface.repository.cart_repository import ICartRepository
from src.domain.interface.repository.order_repository import IOrderRepository
from src.infrastructure.data.session.base import get_session
from src.infrastructure.data.repository.user_repository import UserRepository
from src.infrastructure.data.repository.product_repository import ProductRepository
from src.infrastructure.data.repository.stock_repository import StockRepository
from src.infrastructure.data.repository.cart_repository import CartRepository
from src.infrastructure.data.repository.order_repository import OrderRepository


# DI provider function
def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> IUserRepository:
    return UserRepository(session)


def get_product_repository(
    session: AsyncSession = Depends(get_session),
) -> IProductRepository:
    return ProductRepository(session)


def get_stock_repository(
    session: AsyncSession = Depends(get_session),
) -> IStockRepository:
    return StockRepository(session)


def get_cart_repository(
    session: AsyncSession = Depends(get_session),
) -> ICartRepository:
    return CartRepository(session)


def get_order_repository(
    session: AsyncSession = Depends(get_session),
) -> IOrderRepository:
    return OrderRepository(session)
