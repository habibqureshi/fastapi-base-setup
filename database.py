from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs import DB_URL


engine = create_engine(DB_URL, echo=True,  pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
