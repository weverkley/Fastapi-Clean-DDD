from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.application.schemas.user_schema import UserCreate, UserRead, UserUpdate
from src.application.interface.service.user_service import IUserService
from src.infrastructure.ioc.service import get_user_service

router = APIRouter()


@router.post("/", response_model=UserRead)
async def create(data: UserCreate, service: IUserService = Depends(get_user_service)):
    user = await service.create(data)
    return user


@router.get("/{id}", response_model=UserRead)
async def get(id: int, service: IUserService = Depends(get_user_service)):
    user = await service.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/", response_model=List[UserRead])
async def list(service: IUserService = Depends(get_user_service)):
    return await service.list()

@router.put("/{id}", response_model=UserRead)
async def update(
    id: int, data: UserUpdate, service: IUserService = Depends(get_user_service)
):
    user = await service.update(id, data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete("/{id}")
async def delete(id: int, service: IUserService = Depends(get_user_service)):
    await service.delete(id)
    return JSONResponse(content="", status_code=status.HTTP_200_OK)
