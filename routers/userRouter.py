from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.userSchema import UserCreate

router = APIRouter(
    prefix="/users",  # Prefix for all user-related routes
    tags=["users"],   # Tag for grouping these routes in the docs
)


@router.get("/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print("hi")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
