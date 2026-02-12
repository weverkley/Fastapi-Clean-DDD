import asyncio
from google.cloud import pubsub_v1
from src.application.dto.messaging.outgoing_event import OutgoingEvent
from src.application.interface.messaging.outgoing_event_publisher import IOutgoingEventPublisher
from src.core.config import settings


class GcpPubSubOutgoingEventPublisher(IOutgoingEventPublisher):
    def __init__(self):
        self._publisher = pubsub_v1.PublisherClient()

    def _topic_path(self, routing_key: str) -> str:
        topic_id = routing_key if routing_key else settings.GCP_PUBSUB_DEFAULT_TOPIC
        return self._publisher.topic_path(settings.GCP_PROJECT_ID, topic_id)

    async def publish(self, event: OutgoingEvent) -> None:
        topic_path = self._topic_path(event.routing_key)
        attributes = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "event_version": str(event.event_version),
            "exchange": event.exchange,
        }
        if event.correlation_id:
            attributes["correlation_id"] = event.correlation_id

        future = self._publisher.publish(
            topic_path,
            data=event.payload.encode("utf-8"),
            **attributes,
        )
        await asyncio.to_thread(future.result)
