from abc import ABC, abstractmethod
from typing import Any

from fastapi import Request
from ...dto.auth_dto import AuthLoginDto


class IAuthService(ABC):

    @abstractmethod
    async def login(self, data: AuthLoginDto, request: Request) -> Any: ...

    @abstractmethod
    async def get_access_token(self, request: Request) -> Any: ...