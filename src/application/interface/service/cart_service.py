from abc import abstractmethod
from src.application.dto.model.cart_schema import CartCreate, CartRead, CartItemInput, CartCheckoutResult


class ICartService:
    @abstractmethod
    async def create(self, data: CartCreate) -> CartRead: ...

    @abstractmethod
    async def get(self, cart_id: int) -> CartRead | None: ...

    @abstractmethod
    async def add_item(self, cart_id: int, item: CartItemInput) -> CartRead | None: ...

    @abstractmethod
    async def checkout(self, cart_id: int) -> CartCheckoutResult | None: ...
