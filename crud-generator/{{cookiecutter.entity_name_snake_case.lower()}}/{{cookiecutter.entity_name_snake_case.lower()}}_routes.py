from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.presentation.api.schemas.{{cookiecutter.entity_name_snake_case.lower()}}_schema import {{cookiecutter.entity_name}}Create, {{cookiecutter.entity_name}}Read, {{cookiecutter.entity_name}}Update
from src.application.dto.model.{{cookiecutter.entity_name_snake_case.lower()}}_schema import {{cookiecutter.entity_name}}Create as {{cookiecutter.entity_name}}CreateDto, {{cookiecutter.entity_name}}Update as {{cookiecutter.entity_name}}UpdateDto
from src.application.interface.service.{{cookiecutter.entity_name_snake_case.lower()}}_service import I{{cookiecutter.entity_name}}Service
from src.infrastructure.ioc.service import get_{{cookiecutter.entity_name_snake_case.lower()}}_service

router = APIRouter()

@router.post("/", response_model={{cookiecutter.entity_name}}Read)
async def create(data: {{cookiecutter.entity_name}}Create, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    item = await service.create({{cookiecutter.entity_name}}CreateDto(**data.model_dump()))
    return {{cookiecutter.entity_name}}Read.model_validate(item)

@router.get("/{id}", response_model={{cookiecutter.entity_name}}Read)
async def get(id: int, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    item = await service.get(id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{{cookiecutter.entity_name}} not found")
    return {{cookiecutter.entity_name}}Read.model_validate(item)

@router.get("/", response_model=List[{{cookiecutter.entity_name}}Read])
async def list(service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    items = await service.list()
    return [{{cookiecutter.entity_name}}Read.model_validate(item) for item in items]

@router.put("/{id}", response_model={{cookiecutter.entity_name}}Read)
async def update(id: int, data: {{cookiecutter.entity_name}}Update, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    item = await service.update(id, {{cookiecutter.entity_name}}UpdateDto(**data.model_dump()))
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{{cookiecutter.entity_name}} not found")
    return {{cookiecutter.entity_name}}Read.model_validate(item)

@router.delete("/{id}")
async def delete(id: int, service: I{{cookiecutter.entity_name}}Service = Depends(get_{{cookiecutter.entity_name_snake_case.lower()}}_service)):
    await service.delete(id)
    return JSONResponse(content="", status_code=status.HTTP_200_OK)
