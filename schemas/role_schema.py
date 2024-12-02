from pydantic import BaseModel
from typing import List

from schemas.permission_schema import Permission


class Role(BaseModel):
    id: int


class RoleWithPermission(Role):
    id: int
    name: str
    permission: List[Permission]
