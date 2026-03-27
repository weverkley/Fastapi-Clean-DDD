import asyncio
import inspect
import logging
from hashlib import sha256
from contextlib import suppress
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from collections.abc import Awaitable, Callable
from src.application.dto.messaging.incoming_event import IncomingEvent
from src.application.interface.messaging.incoming_event_adapter import IIncomingEventAdapter

logger = logging.getLogger("consumer.user_created.rabbitmq")


async def _invoke_callback(callback: Callable[[], object] | None) -> None:
    if callback is None:
        return
    maybe_awaitable = callback()
    if inspect.isawaitable(maybe_awaitable):
        await maybe_awaitable


class RabbitMqIncomingEventAdapter(IIncomingEventAdapter):
    def __init__(
        self,
        *,
        rabbitmq_url: str,
        exchange: str,
        queue: str,
        routing_key: str,
        dlx_exchange: str,
        dlq: str,
        dlq_routing_key: str,
    ):
        self._rabbitmq_url = rabbitmq_url
        self._exchange = exchange
        self._queue = queue
        self._routing_key = routing_key
        self._dlx_exchange = dlx_exchange
        self._dlq = dlq
        self._dlq_routing_key = dlq_routing_key

    async def consume(self, on_event: Callable[[IncomingEvent], Awaitable[None]]) -> None:
        async def handle_message(message: AbstractIncomingMessage) -> None:
            payload = message.body.decode("utf-8")
            headers = message.headers or {}
            header_event_id = headers.get("event_id")
            event_id = str(header_event_id) if header_event_id is not None else None
            fallback_key = sha256(f"{message.type or ''}:{payload}".encode("utf-8")).hexdigest()
            message_key = message.message_id or event_id or fallback_key
            event = IncomingEvent(
                message_id=message_key,
                idempotency_key=message_key,
                payload=payload,
                source="rabbitmq",
                event_type=message.type,
                correlation_id=message.correlation_id,
                ack=message.ack,
                nack=lambda: message.nack(requeue=False),
            )
            try:
                await on_event(event)
                await _invoke_callback(event.ack)
            except Exception:
                logger.exception("Failed to process RabbitMQ message message_id=%s", event.message_id)
                await _invoke_callback(event.nack)

        connection = await aio_pika.connect_robust(self._rabbitmq_url)
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=20)

        exchange = await channel.declare_exchange(
            self._exchange,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )
        dlx = await channel.declare_exchange(
            self._dlx_exchange,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )
        queue = await channel.declare_queue(
            self._queue,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self._dlx_exchange,
                "x-dead-letter-routing-key": self._dlq_routing_key,
            },
        )
        dead_queue = await channel.declare_queue(
            self._dlq,
            durable=True,
        )
        await queue.bind(exchange, routing_key=self._routing_key)
        await dead_queue.bind(dlx, routing_key=self._dlq_routing_key)
        consumer_tag = await queue.consume(handle_message)

        logger.info("RabbitMQ consumer running queue=%s routing_key=%s", self._queue, self._routing_key)
        try:
            await asyncio.Future()
        finally:
            with suppress(Exception):
                await queue.cancel(consumer_tag)
            with suppress(Exception):
                await channel.close()
            with suppress(Exception):
                await connection.close()
