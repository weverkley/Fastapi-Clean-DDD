from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.interface.repository.processed_message_repository import IProcessedMessageRepository


class ProcessedMessageRepository(IProcessedMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def try_begin_processing(self, consumer_name: str, message_id: str) -> bool:
        stmt = text(
            """
            INSERT INTO processed_messages (
                consumer_name,
                message_id,
                status,
                first_seen_at,
                processed_at,
                last_error,
                attempt_count
            )
            VALUES (
                :consumer_name,
                :message_id,
                'processing',
                NOW(),
                NULL,
                NULL,
                1
            )
            ON CONFLICT (consumer_name, message_id) DO NOTHING
            RETURNING id
            """
        )
        result = await self.session.execute(
            stmt,
            {
                "consumer_name": consumer_name,
                "message_id": message_id,
            },
        )
        created = result.scalar_one_or_none() is not None
        if created:
            return True

        # Track duplicate delivery attempts for observability.
        attempts_stmt = text(
            """
            UPDATE processed_messages
            SET attempt_count = attempt_count + 1
            WHERE consumer_name = :consumer_name
              AND message_id = :message_id
            """
        )
        await self.session.execute(
            attempts_stmt,
            {
                "consumer_name": consumer_name,
                "message_id": message_id,
            },
        )
        return False

    async def mark_processed(self, consumer_name: str, message_id: str) -> None:
        stmt = text(
            """
            UPDATE processed_messages
            SET status = 'processed',
                processed_at = NOW(),
                last_error = NULL
            WHERE consumer_name = :consumer_name
              AND message_id = :message_id
            """
        )
        await self.session.execute(
            stmt,
            {
                "consumer_name": consumer_name,
                "message_id": message_id,
            },
        )

    async def mark_failed(self, consumer_name: str, message_id: str, error: str) -> None:
        stmt = text(
            """
            UPDATE processed_messages
            SET status = 'failed',
                last_error = :error
            WHERE consumer_name = :consumer_name
              AND message_id = :message_id
            """
        )
        await self.session.execute(
            stmt,
            {
                "consumer_name": consumer_name,
                "message_id": message_id,
                "error": error[:2000],
            },
        )
