import logging
from src.application.dto.messaging.incoming_event import IncomingEvent
from src.application.interface.messaging.processed_message_store import IProcessedMessageStore

logger = logging.getLogger("consumer.user_created")


class UserCreatedEventHandler:
    def __init__(self, store: IProcessedMessageStore, consumer_name: str):
        self._store = store
        self._consumer_name = consumer_name

    async def handle(self, event: IncomingEvent) -> None:
        message_key = event.idempotency_key
        should_process = await self._store.try_begin_processing(self._consumer_name, message_key)
        if not should_process:
            logger.info("Skipping duplicate %s message key=%s", event.source, message_key)
            return

        try:
            logger.info("Consumed %s event key=%s payload=%s", event.source, message_key, event.payload)
            await self._store.mark_processed(self._consumer_name, message_key)
        except Exception as exc:
            await self._store.mark_failed(self._consumer_name, message_key, str(exc))
            raise
