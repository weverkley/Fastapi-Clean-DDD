import json
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
from src.application.dto.model.cart_schema import CartCheckoutResult, CartCreate, CartItemInput, CartItemRead, CartRead
from src.application.interface.service.cart_service import ICartService
from src.core.config import settings
from src.domain.entity.cart_entity import CartEntity
from src.domain.entity.outbox_message_entity import OutboxMessageEntity
from src.domain.interface.repository.cart_repository import ICartRepository
from src.domain.interface.repository.outbox_repository import IOutboxRepository
from src.domain.interface.repository.product_repository import IProductRepository


class CartService(ICartService):
    def __init__(
        self,
        cart_repo: ICartRepository,
        product_repo: IProductRepository,
        outbox_repo: IOutboxRepository,
    ):
        self._cart_repo = cart_repo
        self._product_repo = product_repo
        self._outbox_repo = outbox_repo

    async def create(self, data: CartCreate) -> CartRead:
        cart = CartEntity()
        cart.user_id = data.user_id
        cart.status = "open"
        cart.total_amount = Decimal("0")
        cart.created_at = datetime.now(timezone.utc)
        cart.updated_at = datetime.now(timezone.utc)

        self._cart_repo.session.add(cart)  # type: ignore[attr-defined]
        await self._cart_repo.session.commit()  # type: ignore[attr-defined]
        await self._cart_repo.session.refresh(cart)  # type: ignore[attr-defined]
        return CartRead(
            id=cart.id or 0,
            user_id=cart.user_id,
            status=cart.status,
            total_amount=cart.total_amount,
            items=[],
        )

    async def get(self, cart_id: int) -> CartRead | None:
        cart = await self._cart_repo.get(cart_id)
        if not cart:
            return None

        items = await self._cart_repo.list_items(cart_id)
        return CartRead(
            id=cart.id or 0,
            user_id=cart.user_id,
            status=cart.status,
            total_amount=cart.total_amount,
            items=[
                CartItemRead(
                    id=item.id or 0,
                    cart_id=item.cart_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in items
            ],
        )

    async def add_item(self, cart_id: int, item: CartItemInput) -> CartRead | None:
        cart = await self._cart_repo.get(cart_id)
        if not cart:
            return None
        if cart.status != "open":
            raise ValueError("Cart is not open for changes.")

        product = await self._product_repo.get(item.product_id)
        if not product:
            raise ValueError("Product not found.")

        await self._cart_repo.add_item(cart_id, item.product_id, item.quantity, float(product.price))
        await self._cart_repo.recalculate_total(cart_id)
        await self._cart_repo.session.commit()  # type: ignore[attr-defined]
        return await self.get(cart_id)

    async def checkout(self, cart_id: int) -> CartCheckoutResult | None:
        cart = await self._cart_repo.get(cart_id)
        if not cart:
            return None
        if cart.status != "open":
            raise ValueError("Cart has already been checked out.")

        items = await self._cart_repo.list_items(cart_id)
        if not items:
            raise ValueError("Cart is empty.")

        total_amount = await self._cart_repo.recalculate_total(cart_id)
        await self._cart_repo.set_status(cart_id, "checkout_requested", float(total_amount))

        payload = {
            "cart_id": cart_id,
            "user_id": cart.user_id,
            "total_amount": str(total_amount),
            "items": [
                {
                    "product_id": i.product_id,
                    "quantity": i.quantity,
                    "unit_price": str(i.unit_price),
                }
                for i in items
            ],
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        }

        outbox = OutboxMessageEntity()
        outbox.event_id = str(uuid4())
        outbox.event_type = "cart.checkout.requested"
        outbox.event_version = 1
        outbox.exchange = settings.RABBITMQ_EXCHANGE
        outbox.routing_key = settings.CART_CHECKOUT_REQUESTED_ROUTING_KEY
        outbox.payload = json.dumps(payload)
        outbox.correlation_id = str(cart_id)
        outbox.status = "pending"
        outbox.attempts = 0
        outbox.available_at = datetime.now(timezone.utc)
        outbox.published_at = None
        outbox.dead_lettered_at = None
        outbox.last_error = None
        outbox.created_at = datetime.now(timezone.utc)
        outbox.updated_at = datetime.now(timezone.utc)
        await self._outbox_repo.add(outbox)

        await self._cart_repo.session.commit()  # type: ignore[attr-defined]
        return CartCheckoutResult(cart_id=cart_id, status="checkout_requested", event_id=outbox.event_id)
