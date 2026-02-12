from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.outbox_message_entity import OutboxMessageEntity
from src.domain.interface.repository.outbox_repository import IOutboxRepository


class OutboxRepository(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, message: OutboxMessageEntity) -> None:
        self.session.add(message)

    async def claim_pending(self, limit: int) -> list[OutboxMessageEntity]:
        stmt = text(
            """
            WITH candidates AS (
                SELECT id
                FROM outbox_messages
                WHERE (
                    status = 'pending'
                    OR (status = 'processing' AND updated_at <= NOW() - INTERVAL '5 minutes')
                )
                  AND available_at <= NOW()
                ORDER BY created_at
                LIMIT :limit
                FOR UPDATE SKIP LOCKED
            )
            UPDATE outbox_messages o
            SET status = 'processing',
                attempts = attempts + 1,
                updated_at = NOW()
            FROM candidates c
            WHERE o.id = c.id
            RETURNING
                o.id, o.event_id, o.event_type, o.event_version,
                o.exchange, o.routing_key, o.payload, o.correlation_id,
                o.status, o.attempts, o.available_at, o.published_at,
                o.last_error, o.created_at, o.updated_at
            """
        )
        result = await self.session.execute(stmt, {"limit": limit})
        rows = result.mappings().all()

        messages: list[OutboxMessageEntity] = []
        for row in rows:
            message = OutboxMessageEntity()
            message.id = row["id"]
            message.event_id = row["event_id"]
            message.event_type = row["event_type"]
            message.event_version = row["event_version"]
            message.exchange = row["exchange"]
            message.routing_key = row["routing_key"]
            message.payload = row["payload"]
            message.correlation_id = row["correlation_id"]
            message.status = row["status"]
            message.attempts = row["attempts"]
            message.available_at = row["available_at"]
            message.published_at = row["published_at"]
            message.last_error = row["last_error"]
            message.created_at = row["created_at"]
            message.updated_at = row["updated_at"]
            messages.append(message)
        return messages

    async def mark_published(self, message_id: int) -> None:
        stmt = text(
            """
            UPDATE outbox_messages
            SET status = 'published',
                published_at = NOW(),
                last_error = NULL,
                updated_at = NOW()
            WHERE id = :id
            """
        )
        await self.session.execute(stmt, {"id": message_id})

    async def mark_failed(self, message_id: int, error: str) -> None:
        retry_delay_seconds = 30
        next_attempt = datetime.now(timezone.utc).timestamp() + retry_delay_seconds
        stmt = text(
            """
            UPDATE outbox_messages
            SET status = 'pending',
                last_error = :error,
                available_at = to_timestamp(:next_attempt),
                updated_at = NOW()
            WHERE id = :id
            """
        )
        await self.session.execute(
            stmt,
            {
                "id": message_id,
                "error": error[:2000],
                "next_attempt": next_attempt,
            },
        )
