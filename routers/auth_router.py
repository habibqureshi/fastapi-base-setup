import email
from logging import Logger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from custom_logger import get_logger
from database import get_db
from models.roles_model import Role
from services.current_user_service import get_current_user

from models.user_model import User
from schemas.user_schema import UserCreateWithRole, UserLogin, UserLoginResponse
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from services.user_service import getUserWithRoleAndPermissions


router = APIRouter(
    prefix="/auth",  # Prefix for all user-related routes
    tags=["auth"],   # Tag for grouping these routes in the docs
)

ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 1  # 1 hour
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
# should be kept secret
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "12345_54321")
JWT_REFRESH_SECRET_KEY = os.getenv(
    "JWT_REFRESH_SECRET_KEY", "Refresh12345_54321Refresh")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_jwt_token(payload: dict, expires_delta: int) -> dict:

    exp_time = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode = {"exp": exp_time, "sub": str(payload)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return dict(token=encoded_jwt, expire=expires_delta)


@router.post("/verify/token")
def getToken(user: UserLogin, logger: Logger = Depends(get_logger), currentUser=Depends(get_current_user)):
    logger.info('verifying token')
    return currentUser


@router.post("/verify/token2")
def getToken2(user: UserLogin, currentUser=Depends(get_current_user)):
    return currentUser


@router.post("/token", dependencies=[])
def getToken(user: UserLogin, db: Session = Depends(get_db), logger: Logger = Depends(get_logger)):
    logger.info("token api call for", user.email)
    dbUser = getUserWithRoleAndPermissions([User.email == user.email], db)
    logger.info("user found", dbUser.email)

    if not dbUser:
        logger.info("user not found")
        raise HTTPException(
            status_code=400, detail=f"User email / password not correct")

    isUserPasswordValid = verify_password(user.password, dbUser.password)
    if not isUserPasswordValid:
        logger.info("password is in correct")
        raise HTTPException(
            status_code=400, detail=f"User email / password not correct")
    user_dict = dbUser.__dict__
    del user_dict['password']
    tokenData = create_jwt_token((dbUser.name, dbUser.email,
                                  dbUser.id), ACCESS_TOKEN_EXPIRE_SECONDS)
    return {
        "token": tokenData['token'],
        "expire_in": tokenData['expire'],
        **user_dict}


@router.post("/register", dependencies=[])
def create_user(user: UserCreateWithRole, logger: Logger = Depends(get_logger), db: Session = Depends(get_db)):
    logger.info("hi", user)
    user.password = get_hashed_password(user.password)
    try:
        new_user = User(name=user.name, email=user.email,
                        password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logger.info("error while creating user", e)
    error_message = str(e)
    raise HTTPException(
        status_code=400, detail=f"Error while creating new user {error_message}")
