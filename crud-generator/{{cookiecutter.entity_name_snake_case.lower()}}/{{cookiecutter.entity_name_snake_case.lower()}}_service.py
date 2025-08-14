from src.application.schemas.{{cookiecutter.entity_name_snake_case.lower()}}_schema import {{cookiecutter.entity_name}}Create, {{cookiecutter.entity_name}}Read, {{cookiecutter.entity_name}}Update
from src.application.service.base import BaseService
from src.domain.entity.{{cookiecutter.entity_name_snake_case.lower()}}_entity import {{cookiecutter.entity_name}}Entity
from src.domain.interface.repository.{{cookiecutter.entity_name_snake_case.lower()}}_repository import I{{cookiecutter.entity_name}}Repository
from src.application.interface.service.{{cookiecutter.entity_name_snake_case.lower()}}_service import I{{cookiecutter.entity_name}}Service

class {{cookiecutter.entity_name}}Service(BaseService[{{cookiecutter.entity_name}}Read, {{cookiecutter.entity_name}}Create, {{cookiecutter.entity_name}}Update], I{{cookiecutter.entity_name}}Service):
    def __init__(self, repo: I{{cookiecutter.entity_name}}Repository):
        super().__init__(repo, {{cookiecutter.entity_name}}Entity, {{cookiecutter.entity_name}}Read)