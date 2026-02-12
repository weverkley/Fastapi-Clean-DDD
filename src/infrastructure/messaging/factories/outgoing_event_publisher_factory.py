from src.application.interface.messaging.outgoing_event_publisher import IOutgoingEventPublisher
from src.core.config import settings


def get_outgoing_event_publisher() -> IOutgoingEventPublisher:
    provider = settings.MESSAGE_BUS_PROVIDER.lower().strip()
    if provider == "gcp_pubsub":
        from src.infrastructure.messaging.adapters.outbound.pubsub_outgoing_event_publisher import (
            GcpPubSubOutgoingEventPublisher,
        )
        return GcpPubSubOutgoingEventPublisher()
    from src.infrastructure.messaging.adapters.outbound.rabbitmq_outgoing_event_publisher import (
        RabbitMqOutgoingEventPublisher,
    )
    return RabbitMqOutgoingEventPublisher()
