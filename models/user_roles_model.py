from sqlalchemy import Column, Boolean, Integer, String, ForeignKey

from database import Base


class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, index=True)
    user = Column("user_id", Integer, ForeignKey("users.id"))
    role = Column("role_id", Integer, ForeignKey("roles.id"))
