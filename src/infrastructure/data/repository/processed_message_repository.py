from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.interface.repository.processed_message_repository import IProcessedMessageRepository


class ProcessedMessageRepository(IProcessedMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, consumer_name: str, message_id: str) -> bool:
        stmt = text(
            """
            SELECT 1
            FROM processed_messages
            WHERE consumer_name = :consumer_name
              AND message_id = :message_id
            LIMIT 1
            """
        )
        result = await self.session.execute(
            stmt,
            {
                "consumer_name": consumer_name,
                "message_id": message_id,
            },
        )
        return result.first() is not None

    async def add(self, consumer_name: str, message_id: str) -> None:
        stmt = text(
            """
            INSERT INTO processed_messages (consumer_name, message_id)
            VALUES (:consumer_name, :message_id)
            ON CONFLICT (consumer_name, message_id) DO NOTHING
            """
        )
        await self.session.execute(
            stmt,
            {
                "consumer_name": consumer_name,
                "message_id": message_id,
            },
        )
