from sqlalchemy import Column, Boolean, Integer, String
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    enable = Column(Boolean, default=1)
    deleted = Column(Boolean, default=0)
