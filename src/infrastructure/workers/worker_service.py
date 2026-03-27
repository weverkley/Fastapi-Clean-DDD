import asyncio
import logging
from collections.abc import Awaitable, Callable

from src.core.config import settings
from src.infrastructure.ioc.mappings import configure_mappings
from src.infrastructure.messaging.consumers.cart_checkout_consumer import run_cart_checkout_consumer
from src.infrastructure.messaging.consumers.order_created_consumer import run_order_created_consumer
from src.infrastructure.messaging.consumers.outbox_publisher_worker import run_outbox_publisher

logger = logging.getLogger("workers.service")

WorkerRunner = Callable[[], Awaitable[None]]
WORKER_RUNNERS: tuple[tuple[str, WorkerRunner], ...] = (
    ("outbox_publisher", run_outbox_publisher),
    ("cart_checkout_consumer", run_cart_checkout_consumer),
    ("order_created_consumer", run_order_created_consumer),
)


async def _run_worker_forever(name: str, runner: WorkerRunner) -> None:
    while True:
        try:
            logger.info("Starting worker task=%s", name)
            await runner()
            logger.warning(
                "Worker task exited unexpectedly task=%s restart_in=%ss",
                name,
                settings.WORKER_RESTART_DELAY_SECONDS,
            )
        except asyncio.CancelledError:
            logger.info("Stopping worker task=%s", name)
            raise
        except Exception:
            logger.exception(
                "Worker task failed task=%s restart_in=%ss",
                name,
                settings.WORKER_RESTART_DELAY_SECONDS,
            )

        await asyncio.sleep(settings.WORKER_RESTART_DELAY_SECONDS)


async def run_worker_service() -> None:
    logger.info(
        "Starting worker service workers=%s",
        ", ".join(name for name, _ in WORKER_RUNNERS),
    )
    async with asyncio.TaskGroup() as task_group:
        for name, runner in WORKER_RUNNERS:
            task_group.create_task(_run_worker_forever(name, runner), name=name)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    configure_mappings()
    asyncio.run(run_worker_service())


if __name__ == "__main__":
    main()
