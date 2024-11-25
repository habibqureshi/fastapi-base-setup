from sqlalchemy import Column, Boolean, Integer, String
from database import Base
from sqlalchemy.orm import relationship
from models.user_roles_model import UserRoles

from models.roles_model import Role


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200))
    roles = relationship(
        "Role", secondary=UserRoles.__tablename__)
    enable = Column(Boolean, default=1)
    deleted = Column(Boolean, default=0)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}' , roles={self.roles}, enable={self.enable} , deleted={self.deleted})>"
