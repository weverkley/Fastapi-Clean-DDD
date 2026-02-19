from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...application.interface.service.auth_service import IAuthService
from ...application.service.auth_service import AuthService
from ...application.service.user_service import UserService
from ...application.service.product_service import ProductService
from ...application.service.stock_service import StockService
from ...application.service.cart_service import CartService
from ...application.service.order_service import OrderService
from ..data.repository.user_repository import UserRepository
from ..data.repository.product_repository import ProductRepository
from ..data.repository.stock_repository import StockRepository
from ..data.repository.cart_repository import CartRepository
from ..data.repository.order_repository import OrderRepository
from ..data.repository.outbox_repository import OutboxRepository
from ..data.session.base import get_session
from .repository import get_user_repository
from ...application.interface.service.user_service import IUserService
from ...application.interface.service.product_service import IProductService
from ...application.interface.service.stock_service import IStockService
from ...application.interface.service.cart_service import ICartService
from ...application.interface.service.order_service import IOrderService


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> IAuthService:
    return AuthService(user_repo)


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> IUserService:
    user_repo = UserRepository(session)
    outbox_repo = OutboxRepository(session)
    return UserService(user_repo, outbox_repo)


def get_product_service(
    session: AsyncSession = Depends(get_session),
) -> IProductService:
    product_repo = ProductRepository(session)
    return ProductService(product_repo)


def get_stock_service(
    session: AsyncSession = Depends(get_session),
) -> IStockService:
    stock_repo = StockRepository(session)
    return StockService(stock_repo)


def get_cart_service(
    session: AsyncSession = Depends(get_session),
) -> ICartService:
    cart_repo = CartRepository(session)
    product_repo = ProductRepository(session)
    outbox_repo = OutboxRepository(session)
    return CartService(cart_repo, product_repo, outbox_repo)


def get_order_service(
    session: AsyncSession = Depends(get_session),
) -> IOrderService:
    order_repo = OrderRepository(session)
    return OrderService(order_repo)
