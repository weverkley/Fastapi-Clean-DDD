from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application.interface.messaging.processed_message_store import IProcessedMessageStore
from src.infrastructure.data.repository.processed_message_repository import ProcessedMessageRepository
from src.infrastructure.data.session.base import engine


class SqlAlchemyProcessedMessageStore(IProcessedMessageStore):
    def __init__(self):
        self._session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def exists(self, consumer_name: str, message_id: str) -> bool:
        async with self._session_factory() as session:
            repo = ProcessedMessageRepository(session)
            async with session.begin():
                return await repo.exists(consumer_name, message_id)

    async def add(self, consumer_name: str, message_id: str) -> None:
        async with self._session_factory() as session:
            repo = ProcessedMessageRepository(session)
            async with session.begin():
                await repo.add(consumer_name, message_id)
