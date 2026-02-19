from src.core.config import settings
from src.application.interface.messaging.incoming_event_adapter import IIncomingEventAdapter
from src.application.handlers.cart_checkout_requested_event_handler import CartCheckoutRequestedEventHandler
from src.infrastructure.messaging.adapters.stores.processed_message_store_adapter import SqlAlchemyProcessedMessageStore
from src.infrastructure.messaging.adapters.inbound.pubsub_incoming_event_adapter import GcpPubSubIncomingEventAdapter
from src.infrastructure.messaging.adapters.inbound.rabbitmq_incoming_event_adapter import RabbitMqIncomingEventAdapter


def _get_incoming_adapter() -> IIncomingEventAdapter:
    provider = settings.MESSAGE_BUS_PROVIDER.lower().strip()
    if provider == "gcp_pubsub":
        return GcpPubSubIncomingEventAdapter(
            project_id=settings.GCP_PROJECT_ID,
            subscription_id=settings.GCP_PUBSUB_CART_CHECKOUT_REQUESTED_SUBSCRIPTION,
        )
    return RabbitMqIncomingEventAdapter(
        rabbitmq_url=settings.RABBITMQ_URL,
        exchange=settings.RABBITMQ_EXCHANGE,
        queue=settings.CART_CHECKOUT_REQUESTED_QUEUE,
        routing_key=settings.CART_CHECKOUT_REQUESTED_ROUTING_KEY,
        dlx_exchange=settings.RABBITMQ_DLX_EXCHANGE,
        dlq=settings.CART_CHECKOUT_REQUESTED_DLQ,
        dlq_routing_key=settings.CART_CHECKOUT_REQUESTED_DLQ_ROUTING_KEY,
    )


async def run_cart_checkout_consumer() -> None:
    store = SqlAlchemyProcessedMessageStore()
    handler = CartCheckoutRequestedEventHandler(store=store, consumer_name="cart_checkout_consumer")
    adapter = _get_incoming_adapter()
    await adapter.consume(handler.handle)
