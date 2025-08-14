from sqlalchemy import (
    BigInteger,
    Index,
    PrimaryKeyConstraint,
    Sequence,
    SmallInteger,
    Table,
    Column,
    String,
    DateTime,
    text,
)
from sqlalchemy.orm import registry
from src.domain.entity.user_entity import UserEntity
from .base import metadata

mapper_registry = registry(metadata=metadata)

UserConfiguration = Table(
    "users_consulta",
    metadata,
    Column(
        "id",
        BigInteger,
        Sequence("users_consulta_iduser_seq"),
        primary_key=True,
        autoincrement=True,
    ),
    Column("nome", String(255), nullable=False),
    Column("email", String(155), nullable=False),
    Column("senha", String(255), nullable=False),
    Column("login", String(100), nullable=False),
    Column(
        "data_cadastro",
        DateTime(True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column("user_cadastro", BigInteger, nullable=False),
    Column(
        "data_alteracao",
        DateTime(True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ),
    Column("user_alteracao", BigInteger, nullable=False),
    Column("status", BigInteger, nullable=False),
    Column("cpf", String(11)),
    Column("restringir_acesso", SmallInteger, server_default=text("'0'::smallint")),
    Column("inicio_acesso", SmallInteger),
    Column("fim_acesso", SmallInteger),
    PrimaryKeyConstraint("id", name="idx_35008_primary"),
    Index("idx_35008_cpf_unique", "cpf", unique=True),
    Index("idx_35008_iduser_unique", "id", unique=True),
)


def map_user():
    """
    Imperatively maps the UserEntity to the physical table.
    """
    mapper_registry.map_imperatively(UserEntity, UserConfiguration)
