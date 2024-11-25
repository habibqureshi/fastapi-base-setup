from pydantic import BaseModel
import re


class Permission(BaseModel):
    id: int
    name: str
    url: str
