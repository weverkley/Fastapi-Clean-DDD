from abc import ABC, abstractmethod
from typing import Sequence
from src.domain.interface.repository.base_repository import IBaseRepository
from src.domain.entity.{{cookiecutter.entity_name_snake_case.lower()}}_entity import {{cookiecutter.entity_name}}Entity

class I{{cookiecutter.entity_name}}Repository(IBaseRepository[{{cookiecutter.entity_name}}Entity], ABC):
    """
    Interface for the {{cookiecutter.entity_name.lower()}} repository.
    """
    pass