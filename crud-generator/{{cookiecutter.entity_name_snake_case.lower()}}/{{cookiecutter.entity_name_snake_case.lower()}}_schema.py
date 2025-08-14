from pydantic import BaseModel
from typing import Optional

class {{cookiecutter.entity_name}}Base(BaseModel):
    # Add your schema attributes here
    pass

class {{cookiecutter.entity_name}}Read({{cookiecutter.entity_name}}Base):
    id: int

    class Config:
        from_attributes = True

class {{cookiecutter.entity_name}}Create({{cookiecutter.entity_name}}Base):
    pass

class {{cookiecutter.entity_name}}Update(BaseModel):
    id: int
    # Add your optional update attributes here
    pass