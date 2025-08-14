from pydantic import BaseModel, EmailStr

class AuthLoginDto(BaseModel):
    email: EmailStr
    password: str
    type: int | None = None