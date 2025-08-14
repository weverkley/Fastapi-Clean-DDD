from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interface.repository.user_repository import IUserRepository
from src.infrastructure.data.session.base import get_session
from src.infrastructure.data.repository.user_repository import UserRepository


# DI provider function
def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> IUserRepository:
    return UserRepository(session)