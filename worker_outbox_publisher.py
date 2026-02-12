import asyncio
from src.infrastructure.messaging.outbox_publisher_worker import run_outbox_publisher


if __name__ == "__main__":
    asyncio.run(run_outbox_publisher())
