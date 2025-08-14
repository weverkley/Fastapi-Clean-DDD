from fastapi import Depends

from ...application.interface.service.auth_service import IAuthService
from ...application.service.auth_service import AuthService
from ...application.service.user_service import UserService
from ..data.repository.user_repository import UserRepository
from .repository import get_user_repository
from ...application.interface.service.user_service import IUserService


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository)
) -> IAuthService:
    return AuthService(user_repo)


def get_user_service(
    repo: UserRepository = Depends(get_user_repository)
) -> IUserService:
    return UserService(repo)
