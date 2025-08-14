from abc import ABC, abstractmethod
from typing import Sequence
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.user_entity import UserEntity

class IUserRepository(IBaseRepository[UserEntity], ABC):
    """
    Interface for the user repository. Inherits from the base repository interface.
    Specific user-related database operations can be defined here.
    """
    
    @abstractmethod
    async def list_last_users(self) -> Sequence[UserEntity]: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserEntity | None: ...