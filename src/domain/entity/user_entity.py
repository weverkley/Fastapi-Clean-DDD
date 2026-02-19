from .base import BaseEntity

class UserEntity(BaseEntity):
    name: str
    email: str
    password: str
    phone_number: str
