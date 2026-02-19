import json
from datetime import datetime, timezone
from uuid import uuid4
from typing import Sequence
from src.application.dto.model.user_schema import UserCreate, UserRead, UserUpdate
from src.application.service.base import BaseService
from src.domain.entity.user_entity import UserEntity
from src.domain.entity.outbox_message_entity import OutboxMessageEntity
from src.domain.interface.repository.user_repository import IUserRepository
from src.domain.interface.repository.outbox_repository import IOutboxRepository
from src.application.interface.service.user_service import IUserService
from src.core.config import settings
from automapper import mapper

class UserService(BaseService[UserRead, UserCreate, UserUpdate], IUserService):
    def __init__(self, repo: IUserRepository, outbox_repo: IOutboxRepository):
        super().__init__(repo, UserEntity, UserRead)
        self._repo: IUserRepository = repo  # Explicitly type the repository
        self._outbox_repo: IOutboxRepository = outbox_repo

    async def list_last_users(self) -> Sequence[UserRead]:
        users = await self._repo.list_last_users()
        return [self._read_schema.model_validate(user) for user in users]

    async def create(self, data: UserCreate) -> UserRead:
        entity = mapper.to(self._entity).map(data)
        self._repo.session.add(entity)  # type: ignore[attr-defined]
        await self._repo.session.flush()  # type: ignore[attr-defined]

        payload = {
            "id": entity.id,
            "name": entity.name,
            "email": entity.email,
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        }

        event = OutboxMessageEntity()
        event.event_id = str(uuid4())
        event.event_type = "user.created"
        event.event_version = 1
        event.exchange = settings.RABBITMQ_EXCHANGE
        event.routing_key = settings.USER_CREATED_ROUTING_KEY
        event.payload = json.dumps(payload)
        event.correlation_id = str(entity.id)
        event.status = "pending"
        event.attempts = 0
        event.available_at = datetime.now(timezone.utc)
        event.published_at = None
        event.dead_lettered_at = None
        event.last_error = None
        event.created_at = datetime.now(timezone.utc)
        event.updated_at = datetime.now(timezone.utc)
        await self._outbox_repo.add(event)

        await self._repo.session.commit()  # type: ignore[attr-defined]
        await self._repo.session.refresh(entity)  # type: ignore[attr-defined]
        return self._read_schema.model_validate(entity)
