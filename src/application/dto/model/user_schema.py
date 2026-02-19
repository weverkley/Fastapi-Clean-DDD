from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr | str
    password: str
    phone_number: str


class UserRead(UserBase):
    id: int | None = None

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    phone_number: Optional[str]
