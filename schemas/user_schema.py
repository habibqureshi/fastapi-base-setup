
from pydantic import BaseModel, EmailStr, validator
import re
from typing import List

from schemas.role_schema import Role, RoleWithPermission


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    token: str
    expire_in: int
    role: List[RoleWithPermission]

    class Config:
        orm_mode = True
        from_attributes = True

    def __init__(self, id: int, name: EmailStr, email: EmailStr, token: str, expire_in: int, role: List[Role]):
        # Manually initialize the attributes
        super().__init__(id=id, name=name, email=email,
                         token=token, expire_in=expire_in, role=role)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @validator('password')
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        if not re.search(r"[A-Z]", password):
            raise ValueError(
                'Password must contain at least one uppercase letter.')
        if not re.search(r"[a-z]", password):
            raise ValueError(
                'Password must contain at least one lowercase letter.')
        if not re.search(r"[0-9]", password):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError(
                'Password must contain at least one special character.')
        return password

    class Config:
        orm_mode = True


class UserCreateWithRole(UserCreate):
    roles: List[Role]

    class Config:
        orm_mode = True
