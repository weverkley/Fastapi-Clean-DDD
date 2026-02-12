import asyncio
from src.infrastructure.messaging.user_created_consumer import run_user_created_consumer


if __name__ == "__main__":
    asyncio.run(run_user_created_consumer())
