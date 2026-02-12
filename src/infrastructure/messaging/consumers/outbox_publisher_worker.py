import asyncio
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application.handlers.publish_outbox_batch_handler import PublishOutboxBatchHandler
from src.core.config import settings
from src.infrastructure.data.repository.outbox_repository import OutboxRepository
from src.infrastructure.data.session.base import engine
from src.infrastructure.messaging.factories.outgoing_event_publisher_factory import (
    get_outgoing_event_publisher,
)

logger = logging.getLogger("outbox.publisher")


async def run_outbox_publisher() -> None:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    publisher = get_outgoing_event_publisher()
    await publisher.start()

    try:
        while True:
            try:
                async with session_factory() as session:
                    repo = OutboxRepository(session)
                    handler = PublishOutboxBatchHandler(
                        outbox_repo=repo,
                        publisher=publisher,
                        max_attempts=settings.OUTBOX_MAX_ATTEMPTS,
                    )
                    await handler.handle(settings.OUTBOX_BATCH_SIZE)
            except Exception:
                logger.exception("Outbox publisher cycle failed")

            await asyncio.sleep(settings.OUTBOX_PUBLISH_INTERVAL_SECONDS)
    finally:
        await publisher.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_outbox_publisher())
