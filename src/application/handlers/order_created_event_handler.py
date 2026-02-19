import json
import logging
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application.dto.messaging.incoming_event import IncomingEvent
from src.application.interface.messaging.processed_message_store import IProcessedMessageStore
from src.core.config import settings
from src.domain.entity.outbox_message_entity import OutboxMessageEntity
from src.infrastructure.data.repository.order_repository import OrderRepository
from src.infrastructure.data.repository.stock_repository import StockRepository
from src.infrastructure.data.session.base import engine

logger = logging.getLogger("consumer.order_created")


class OrderCreatedEventHandler:
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
            order_id = int(payload["order_id"])
            items = payload["items"]

            async with self._session_factory() as session:
                order_repo = OrderRepository(session)
                stock_repo = StockRepository(session)

                async with session.begin():
                    await order_repo.set_status(order_id, "completed")
                    for item in items:
                        await stock_repo.mark_sold(int(item["product_id"]), int(item["quantity"]))

                    outbox = OutboxMessageEntity()
                    outbox.event_id = str(uuid4())
                    outbox.event_type = "order.completed"
                    outbox.event_version = 1
                    outbox.exchange = settings.RABBITMQ_EXCHANGE
                    outbox.routing_key = settings.ORDER_COMPLETED_ROUTING_KEY
                    outbox.payload = json.dumps(
                        {
                            "order_id": order_id,
                            "status": "completed",
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
            logger.info("Processed order created event order_id=%s", order_id)
        except Exception as exc:
            await self._store.mark_failed(self._consumer_name, message_key, str(exc))
            raise
