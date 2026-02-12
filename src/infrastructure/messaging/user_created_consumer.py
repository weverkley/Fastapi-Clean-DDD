import asyncio
import logging
import aio_pika
from aio_pika.abc import AbstractIncomingMessage
from src.core.config import settings

logger = logging.getLogger("consumer.user_created")


async def handle_user_created(message: AbstractIncomingMessage) -> None:
    async with message.process(requeue=False):
        payload = message.body.decode("utf-8")
        logger.info(
            "Consumed event type=%s message_id=%s payload=%s",
            message.type,
            message.message_id,
            payload,
        )


async def run_user_created_consumer() -> None:
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=20)

    exchange = await channel.declare_exchange(
        settings.RABBITMQ_EXCHANGE,
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )
    queue = await channel.declare_queue(
        settings.USER_CREATED_QUEUE,
        durable=True,
    )
    await queue.bind(exchange, routing_key=settings.USER_CREATED_ROUTING_KEY)
    await queue.consume(handle_user_created)

    logger.info(
        "Consumer running queue=%s routing_key=%s",
        settings.USER_CREATED_QUEUE,
        settings.USER_CREATED_ROUTING_KEY,
    )
    await asyncio.Future()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_user_created_consumer())
