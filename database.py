from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL format: mysql+pymysql://user:password@host/dbname
DATABASE_URL = "mysql+pymysql://root@localhost/test"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
