from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entity.{{cookiecutter.entity_name_snake_case.lower()}}_entity import {{cookiecutter.entity_name}}Entity
from src.infrastructure.data.repository.base import BaseRepository
from src.domain.interface.repository.{{cookiecutter.entity_name_snake_case.lower()}}_repository import I{{cookiecutter.entity_name}}Repository

class {{cookiecutter.entity_name}}Repository(BaseRepository[{{cookiecutter.entity_name}}Entity], I{{cookiecutter.entity_name}}Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, {{cookiecutter.entity_name}}Entity)