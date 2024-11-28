from logging import Logger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from custom_logger import get_logger
from database import get_db
from models.user_model import User
from schemas.user_schema import UserCreate

router = APIRouter(
    prefix="/users",  # Prefix for all user-related routes
    tags=["users"],   # Tag for grouping these routes in the docs
)


@router.get("/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), logger: Logger = Depends(get_logger)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db), logger: Logger = Depends(get_logger)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
