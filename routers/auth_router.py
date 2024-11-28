from logging import Logger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from custom_logger import get_logger
from database import get_db
from models.roles_model import Role
from services.auth_service import generate_token, genreate_user
from services.current_user_service import get_current_user
from models.user_model import User
from schemas.user_schema import UserCreateWithRole, UserLogin


from services.user_service import getUserWithRoleAndPermissions


router = APIRouter(
    prefix="/auth",  # Prefix for all user-related routes
    tags=["auth"],   # Tag for grouping these routes in the docs
)


@router.post("/verify/token")
def getToken(user: UserLogin, logger: Logger = Depends(get_logger), currentUser=Depends(get_current_user)):
    logger.info('verifying token')
    return currentUser


@router.post("/verify/token2")
def getToken2(user: UserLogin, currentUser=Depends(get_current_user)):
    return currentUser


@router.post("/token")
def getToken(user: UserLogin, db: Session = Depends(get_db), logger=Depends(get_logger)):
    return generate_token(user, db)


@router.post("/register")
def create_user(user: UserCreateWithRole, logger: Logger = Depends(get_logger), db: Session = Depends(get_db)):
    logger.info(f'creating new user {user}')
    return genreate_user(user, logger, db)
