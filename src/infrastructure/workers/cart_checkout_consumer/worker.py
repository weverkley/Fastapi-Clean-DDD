import asyncio
from src.infrastructure.ioc.mappings import configure_mappings
from src.infrastructure.messaging.consumers.cart_checkout_consumer import run_cart_checkout_consumer


if __name__ == "__main__":
    configure_mappings()
    asyncio.run(run_cart_checkout_consumer())
