import jwt
import requests
from typing import Any
from fastapi import Request

from ..dto.auth_dto import AuthLoginDto
from ...domain.exception.permission_denied_exception import PermissionDeniedException
from ...domain.interface.repository.user_repository import IUserRepository
from ..interface.service.auth_service import IAuthService
from src.core.config import settings
from automapper import mapper


class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository):
        self._user_repo = user_repo

    async def login(self, data: AuthLoginDto, request: Request) -> Any:
        permit_token = request.headers.get("permittoken")
        token_permissions: str | None = permit_token

        user_consulta = await self._user_repo.get_user_by_email(data.email)
            
        if user_consulta == None:
            raise PermissionDeniedException("Usuário não encontrado.")

        user_dados = {
            "user": user_consulta.id,
            "email": data.email,
            "tipo": 1,
            "nome_user": user_consulta.nome,
            "token_permissoes": token_permissions,
        }

        token = jwt.encode(user_dados, settings.SECRET_KEY, algorithm="HS256")

        return {
            "id": user_consulta.id,
            "nome": user_consulta.nome,
            "email": data.email,
            "tipo": 1,
            "token": token
        }
        
    async def get_access_token(self, request: Request) -> Any:
        pass