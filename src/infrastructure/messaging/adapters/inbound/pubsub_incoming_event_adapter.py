import asyncio
import logging
from contextlib import suppress
from hashlib import sha256
from collections.abc import Awaitable, Callable
from google.cloud import pubsub_v1
from src.application.dto.messaging.incoming_event import IncomingEvent
from src.application.interface.messaging.incoming_event_adapter import IIncomingEventAdapter

logger = logging.getLogger("consumer.user_created.gcp_pubsub")


class GcpPubSubIncomingEventAdapter(IIncomingEventAdapter):
    def __init__(self, *, project_id: str, subscription_id: str):
        self._project_id = project_id
        self._subscription_id = subscription_id
        self._subscriber = pubsub_v1.SubscriberClient()

    async def consume(self, on_event: Callable[[IncomingEvent], Awaitable[None]]) -> None:
        loop = asyncio.get_running_loop()
        subscription_path = self._subscriber.subscription_path(self._project_id, self._subscription_id)

        async def process_message(message: pubsub_v1.subscriber.message.Message) -> None:
            message_id = message.message_id or sha256(message.data).hexdigest()
            attributes = message.attributes or {}
            event = IncomingEvent(
                message_id=message_id,
                payload=message.data.decode("utf-8"),
                source="pubsub",
                event_type=attributes.get("event_type"),
                correlation_id=attributes.get("correlation_id"),
                ack=message.ack,
                nack=message.nack,
            )
            try:
                await on_event(event)
                if event.ack:
                    event.ack()
            except Exception:
                logger.exception("Failed to process Pub/Sub message message_id=%s", event.message_id)
                if event.nack:
                    event.nack()

        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            loop.create_task(process_message(message))

        streaming_pull_future = self._subscriber.subscribe(subscription_path, callback=callback)
        logger.info("GCP Pub/Sub consumer running subscription=%s", subscription_path)

        try:
            await asyncio.to_thread(streaming_pull_future.result)
        finally:
            streaming_pull_future.cancel()
            with suppress(Exception):
                await asyncio.to_thread(streaming_pull_future.result, timeout=2)
            self._subscriber.close()
