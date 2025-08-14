from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    nome: str
    email: EmailStr | str
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

class UserRead(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    id: int
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    login: Optional[str]
    data_cadastro: Optional[datetime]
    user_cadastro: Optional[int]
    data_alteracao: Optional[datetime]
    user_alteracao: Optional[int]
    status: Optional[int]
    cpf: Optional[str]
    restringir_acesso: Optional[int]
    inicio_acesso: Optional[int]
    fim_acesso: Optional[int]

