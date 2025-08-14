from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.application.schemas.{{cookiecutter.entity_name_snake_case.lower()}}_schema import {{cookiecutter.entity_name}}Create, {{cookiecutter.entity_name}}Read, {{cookiecutter.entity_name}}Update
from src.application.interface.service.{{cookiecutter.entity_name_snake_case.lower()}}_service import I{{cookiecutter.entity_name}}Service
from src.infrastructure.ioc.service import get_{{cookiecutter.entity_name_snake_case.lower()}}_service

router = APIRouter()

@router.post("/", response_model={{cookiecutter.entity_name}}Read)
async def create(data: {{cookiecutter.entity_name}}Create, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    return await service.create(data)

@router.get("/{id}", response_model={{cookiecutter.entity_name}}Read)
async def get(id: int, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    item = await service.get(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{{cookiecutter.entity_name}} not found")
    return item

@router.get("/", response_model=List[{{cookiecutter.entity_name}}Read])
async def list(service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    return await service.list()

@router.put("/{id}", response_model={{cookiecutter.entity_name}}Read)
async def update(id: int, data: {{cookiecutter.entity_name}}Update, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    item = await service.update(id, data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{{cookiecutter.entity_name}} not found")
    return item

@router.delete("/{id}")
async def delete(id: int, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    await service.delete(id)
    return JSONResponse(content="", status_code=status.HTTP_200_OK)