from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from src.domain.entity.user_entity import UserEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

UserConfiguration = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("phone_number", String(30), nullable=False),
)


def map_user():
    """
    Imperatively maps the UserEntity to the physical table.
    """
    mapper_registry.map_imperatively(UserEntity, UserConfiguration)
