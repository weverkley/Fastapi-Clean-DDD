import json
import logging
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application.dto.messaging.incoming_event import IncomingEvent
from src.application.interface.messaging.processed_message_store import IProcessedMessageStore
from src.core.config import settings
from src.domain.entity.order_entity import OrderEntity
from src.domain.entity.outbox_message_entity import OutboxMessageEntity
from src.infrastructure.data.repository.cart_repository import CartRepository
from src.infrastructure.data.repository.order_repository import OrderRepository
from src.infrastructure.data.repository.stock_repository import StockRepository
from src.infrastructure.data.session.base import engine

logger = logging.getLogger("consumer.cart_checkout")


class CartCheckoutRequestedEventHandler:
    def __init__(self, store: IProcessedMessageStore, consumer_name: str):
        self._store = store
        self._consumer_name = consumer_name
        self._session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def handle(self, event: IncomingEvent) -> None:
        message_key = event.idempotency_key
        should_process = await self._store.try_begin_processing(self._consumer_name, message_key)
        if not should_process:
            logger.info("Skipping duplicate message key=%s", message_key)
            return

        try:
            payload = json.loads(event.payload)
            cart_id = int(payload["cart_id"])
            user_id = int(payload["user_id"])
            items = payload["items"]
            total_amount = Decimal(str(payload["total_amount"]))

            async with self._session_factory() as session:
                stock_repo = StockRepository(session)
                order_repo = OrderRepository(session)
                cart_repo = CartRepository(session)

                async with session.begin():
                    existing_order = await order_repo.get_by_cart_id(cart_id)
                    if existing_order is None:
                        for item in items:
                            reserved = await stock_repo.reserve(int(item["product_id"]), int(item["quantity"]))
                            if not reserved:
                                raise ValueError(f"Insufficient stock for product {item['product_id']}")

                        order = OrderEntity()
                        order.cart_id = cart_id
                        order.user_id = user_id
                        order.status = "created"
                        order.total_amount = total_amount
                        order.created_at = datetime.now(timezone.utc)
                        order.updated_at = datetime.now(timezone.utc)
                        session.add(order)
                        await session.flush()
                        order_id = int(order.id or 0)
                    else:
                        order_id = int(existing_order.id or 0)

                    await cart_repo.set_status(cart_id, "ordered", float(total_amount))

                    outbox = OutboxMessageEntity()
                    outbox.event_id = str(uuid4())
                    outbox.event_type = "order.created"
                    outbox.event_version = 1
                    outbox.exchange = settings.RABBITMQ_EXCHANGE
                    outbox.routing_key = settings.ORDER_CREATED_ROUTING_KEY
                    outbox.payload = json.dumps(
                        {
                            "order_id": order_id,
                            "cart_id": cart_id,
                            "user_id": user_id,
                            "total_amount": str(total_amount),
                            "items": items,
                            "occurred_at": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                    outbox.correlation_id = str(order_id)
                    outbox.status = "pending"
                    outbox.attempts = 0
                    outbox.available_at = datetime.now(timezone.utc)
                    outbox.published_at = None
                    outbox.dead_lettered_at = None
                    outbox.last_error = None
                    outbox.created_at = datetime.now(timezone.utc)
                    outbox.updated_at = datetime.now(timezone.utc)
                    session.add(outbox)

            await self._store.mark_processed(self._consumer_name, message_key)
            logger.info("Processed cart checkout request cart_id=%s", cart_id)
        except Exception as exc:
            await self._store.mark_failed(self._consumer_name, message_key, str(exc))
            raise
