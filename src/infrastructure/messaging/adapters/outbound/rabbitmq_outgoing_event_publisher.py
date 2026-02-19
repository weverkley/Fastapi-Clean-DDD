import aio_pika
from aio_pika import DeliveryMode, Message
from src.application.dto.messaging.outgoing_event import OutgoingEvent
from src.application.interface.messaging.outgoing_event_publisher import IOutgoingEventPublisher
from src.core.config import settings


class RabbitMqOutgoingEventPublisher(IOutgoingEventPublisher):
    def __init__(self):
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None
        self._exchanges: dict[str, aio_pika.abc.AbstractExchange] = {}

    async def start(self) -> None:
        if self._connection and not self._connection.is_closed:
            return
        self._connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=50)

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None
        self._exchanges = {}

    async def _get_exchange(self, exchange: str) -> aio_pika.abc.AbstractExchange:
        if not self._channel:
            await self.start()
        assert self._channel is not None
        if exchange not in self._exchanges:
            self._exchanges[exchange] = await self._channel.declare_exchange(
                exchange,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
        return self._exchanges[exchange]

    async def publish(self, event: OutgoingEvent) -> None:
        exchange_obj = await self._get_exchange(event.exchange)
        message = Message(
            body=event.payload.encode("utf-8"),
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,
            message_id=event.event_id,
            correlation_id=event.correlation_id,
            type=event.event_type,
            headers={
                "event_id": event.event_id,
                "event_version": event.event_version,
            },
        )
        await exchange_obj.publish(message, routing_key=event.routing_key)
