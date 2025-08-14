from datetime import datetime
from .base import BaseEntity

class UserEntity(BaseEntity):
    nome: str
    email: str
    senha: str
    login: str
    data_cadastro: datetime
    user_cadastro: int
    data_alteracao: datetime
    user_alteracao: int
    status: int
    cpf: str
    restringir_acesso: int
    inicio_acesso: int
    fim_acesso: int