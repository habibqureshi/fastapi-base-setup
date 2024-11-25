from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from database import Base


class RolePermission(Base):
    __tablename__ = 'role_permission'

    id = Column(Integer, primary_key=True, index=True)
    role = Column("role_id", Integer, ForeignKey("roles.id"))
    permission = Column("permission_id", Integer, ForeignKey("permissions.id"))
