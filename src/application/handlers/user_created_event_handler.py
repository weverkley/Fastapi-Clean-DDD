import logging
from src.application.dto.messaging.incoming_event import IncomingEvent
from src.application.interface.messaging.processed_message_store import IProcessedMessageStore

logger = logging.getLogger("consumer.user_created")


class UserCreatedEventHandler:
    def __init__(self, store: IProcessedMessageStore, consumer_name: str):
        self._store = store
        self._consumer_name = consumer_name

    async def handle(self, event: IncomingEvent) -> None:
        already_processed = await self._store.exists(self._consumer_name, event.message_id)
        if already_processed:
            logger.info("Skipping duplicate %s message message_id=%s", event.source, event.message_id)
            return

        logger.info("Consumed %s event message_id=%s payload=%s", event.source, event.message_id, event.payload)
        await self._store.add(self._consumer_name, event.message_id)
