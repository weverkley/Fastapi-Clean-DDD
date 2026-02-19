import asyncio
from src.infrastructure.ioc.mappings import configure_mappings
from src.infrastructure.messaging.consumers.outbox_publisher_worker import run_outbox_publisher


if __name__ == "__main__":
    configure_mappings()
    asyncio.run(run_outbox_publisher())
