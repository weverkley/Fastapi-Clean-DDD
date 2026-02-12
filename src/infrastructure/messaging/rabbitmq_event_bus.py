import aio_pika
from aio_pika import DeliveryMode, Message
from src.application.interface.messaging.event_bus import IEventBus
from src.core.config import settings


class RabbitMQEventBus(IEventBus):
    async def publish(
        self,
        *,
        exchange: str,
        routing_key: str,
        payload: str,
        event_id: str,
        event_type: str,
        event_version: int,
        correlation_id: str | None = None,
    ) -> None:
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        try:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=50)
            exchange_obj = await channel.declare_exchange(
                exchange,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            message = Message(
                body=payload.encode("utf-8"),
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
                message_id=event_id,
                correlation_id=correlation_id,
                type=event_type,
                headers={"event_version": event_version},
            )
            await exchange_obj.publish(message, routing_key=routing_key)
        finally:
            await connection.close()
