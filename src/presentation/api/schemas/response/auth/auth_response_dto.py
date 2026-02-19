from pydantic import BaseModel, EmailStr


class AuthResponseDto(BaseModel):
    email: EmailStr
    id: int
    name: str
    tipo: int
    token: str
