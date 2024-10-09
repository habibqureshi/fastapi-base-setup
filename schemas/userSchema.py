from dataclasses import Field
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
