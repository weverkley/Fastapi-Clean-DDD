import asyncio
from src.infrastructure.ioc.mappings import configure_mappings
from src.infrastructure.messaging.consumers.order_created_consumer import run_order_created_consumer


if __name__ == "__main__":
    configure_mappings()
    asyncio.run(run_order_created_consumer())
