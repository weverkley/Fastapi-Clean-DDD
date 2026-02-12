import asyncio
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.core.config import settings
from src.infrastructure.data.repository.outbox_repository import OutboxRepository
from src.infrastructure.data.session.base import engine
from src.infrastructure.messaging.rabbitmq_event_bus import RabbitMQEventBus

logger = logging.getLogger("outbox.publisher")


async def run_outbox_publisher() -> None:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    event_bus = RabbitMQEventBus()

    while True:
        try:
            async with session_factory() as session:
                repo = OutboxRepository(session)
                async with session.begin():
                    messages = await repo.claim_pending(settings.OUTBOX_BATCH_SIZE)

                for message in messages:
                    try:
                        await event_bus.publish(
                            exchange=message.exchange,
                            routing_key=message.routing_key,
                            payload=message.payload,
                            event_id=message.event_id,
                            event_type=message.event_type,
                            event_version=message.event_version,
                            correlation_id=message.correlation_id,
                        )
                        async with session.begin():
                            await repo.mark_published(message.id)  # type: ignore[arg-type]
                    except Exception as exc:
                        logger.exception("Failed to publish outbox message %s", message.event_id)
                        async with session.begin():
                            await repo.mark_failed(message.id, str(exc))  # type: ignore[arg-type]
        except Exception:
            logger.exception("Outbox publisher cycle failed")

        await asyncio.sleep(settings.OUTBOX_PUBLISH_INTERVAL_SECONDS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_outbox_publisher())
