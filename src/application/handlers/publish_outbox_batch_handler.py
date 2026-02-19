import logging
from src.application.dto.messaging.outgoing_event import OutgoingEvent
from src.application.interface.messaging.outgoing_event_publisher import IOutgoingEventPublisher
from src.domain.interface.repository.outbox_repository import IOutboxRepository

logger = logging.getLogger("outbox.publisher.handler")


class PublishOutboxBatchHandler:
    def __init__(
        self,
        outbox_repo: IOutboxRepository,
        publisher: IOutgoingEventPublisher,
        max_attempts: int,
    ):
        self._outbox_repo = outbox_repo
        self._publisher = publisher
        self._max_attempts = max_attempts

    async def handle(self, batch_size: int) -> int:
        messages = await self._outbox_repo.claim_pending(batch_size)
        for message in messages:
            try:
                event = OutgoingEvent(
                    event_id=message.event_id,
                    event_type=message.event_type,
                    event_version=message.event_version,
                    exchange=message.exchange,
                    routing_key=message.routing_key,
                    payload=message.payload,
                    correlation_id=message.correlation_id,
                )
                await self._publisher.publish(event)
                await self._outbox_repo.mark_published(message.id)  # type: ignore[arg-type]
            except Exception as exc:
                await self._outbox_repo.rollback()
                try:
                    await self._outbox_repo.mark_failed(
                        message.id,  # type: ignore[arg-type]
                        str(exc),
                        self._max_attempts,
                    )
                except Exception:
                    await self._outbox_repo.rollback()
                    logger.exception("Failed to mark outbox message as failed message_id=%s", message.id)
        return len(messages)
