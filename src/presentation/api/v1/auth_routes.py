from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from ....application.dto.auth_dto import AuthLoginDto
from ....application.interface.service.auth_service import IAuthService
from ....infrastructure.ioc.service import get_auth_service

router = APIRouter()


@router.post("/login", response_model=Any)
async def login(request: Request, data: AuthLoginDto, service: IAuthService = Depends(get_auth_service)):
    user = await service.login(data, request)
    if "error" in user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=user["error"])
    return user

@router.post("/getAccessToken", response_model=Any)
async def get_access_token(request: Request, service: IAuthService = Depends(get_auth_service)):
    user = await service.get_access_token(request)
    if "error" in user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=user["error"])
    return user