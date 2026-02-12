from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from ....presentation.api.schemas.request.auth.auth_dto import AuthLoginDto
from ....presentation.api.schemas.response.auth.auth_response_dto import AuthResponseDto
from ....application.dto.request.auth.auth_dto import AuthLoginDto as AuthLoginDtoRequest
from ....application.interface.service.auth_service import IAuthService
from ....infrastructure.ioc.service import get_auth_service

router = APIRouter()


@router.post("/login", response_model=AuthResponseDto)
async def login(request: Request, data: AuthLoginDto, service: IAuthService = Depends(get_auth_service)):
    request_data = AuthLoginDtoRequest(**data.model_dump())
    user = await service.login(request_data, request)
    if "error" in user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=user["error"])
    return AuthResponseDto.model_validate(user)

@router.post("/getAccessToken", response_model=Any)
async def get_access_token(request: Request, service: IAuthService = Depends(get_auth_service)):
    user = await service.get_access_token(request)
    if user is None:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Access token endpoint is not implemented")
    if "error" in user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=user["error"])
    return user
