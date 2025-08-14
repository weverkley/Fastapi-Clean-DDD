from abc import ABC, abstractmethod
from typing import Sequence
from src.application.interface.service.base_service import IBaseService
from src.application.schemas.user_schema import UserRead, UserCreate, UserUpdate

class IUserService(IBaseService[UserRead, UserCreate, UserUpdate], ABC):

    @abstractmethod
    async def list_last_users(self) -> Sequence[UserRead]: ...