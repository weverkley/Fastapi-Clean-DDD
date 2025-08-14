from typing import Sequence
from src.application.schemas.user_schema import UserCreate, UserRead, UserUpdate
from src.application.service.base import BaseService
from src.domain.entity.user_entity import UserEntity
from src.domain.interface.repository.user_repository import IUserRepository
from src.application.interface.service.user_service import IUserService
from automapper import mapper

class UserService(BaseService[UserRead, UserCreate, UserUpdate], IUserService):
    def __init__(self, repo: IUserRepository):
        super().__init__(repo, UserEntity, UserRead)
        self._repo: IUserRepository = repo  # Explicitly type the repository

    async def list_last_users(self) -> Sequence[UserRead]:
        users = await self._repo.list_last_users()
        return [self._read_schema.model_validate(user) for user in users]