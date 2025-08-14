from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.user_entity import UserEntity
from src.infrastructure.data.repository.base import BaseRepository
from src.domain.interface.repository.user_repository import IUserRepository
from sqlalchemy import select, desc

class UserRepository(BaseRepository[UserEntity], IUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserEntity)

    async def list_last_users(self) -> Sequence[UserEntity]:
        """
        Retrieve the last users from the database.
        This method can be customized to include specific filtering or ordering logic.
        """

        stmt = select(self.model).order_by(desc(getattr(self.model, "data_cadastro"))).limit(10)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        stmt = select(self.model).where(self.model.email == email) # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
