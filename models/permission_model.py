from sqlalchemy import Column, Boolean, Integer, String
from database import Base


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    url = Column(String(100), index=True)

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name='{self.name}' , url={self.url})>"
