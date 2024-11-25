from sqlalchemy import Column, Boolean, Integer, String
from database import Base
from sqlalchemy.orm import relationship
from models.role_permission_model import RolePermission
from models.permission_model import Permission


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    permissions = relationship(
        "Permission", secondary=RolePermission.__tablename__)
    enable = Column(Boolean, default=1)
    deleted = Column(Boolean, default=0)

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}' , permission = {self.permissions}, enable={self.enable} , deleted={self.deleted})>"
