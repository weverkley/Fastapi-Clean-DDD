from pydantic import BaseModel, EmailStr


class AuthResponseDto(BaseModel):
    email: EmailStr
    id: int
    nome: str
    tipo: int
    token: str
