from abc import ABC, abstractmethod
from typing import Sequence
from src.application.interface.service.base_service import IBaseService
from src.application.schemas.{{cookiecutter.entity_name_snake_case.lower()}}_schema import {{cookiecutter.entity_name}}Read, {{cookiecutter.entity_name}}Create, {{cookiecutter.entity_name}}Update

class I{{cookiecutter.entity_name}}Service(IBaseService[{{cookiecutter.entity_name}}Read, {{cookiecutter.entity_name}}Create, {{cookiecutter.entity_name}}Update], ABC):
    pass