
from logging import Logger
from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from custom_logger import get_logger
from database import get_db
from fastapi import Depends

from models.user_model import User
from schemas.user_schema import UserLogin
from fastapi import HTTPException
import os
from fastapi.responses import JSONResponse
from schemas.user_schema import UserCreateWithRole
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from services.user_service import create_new_user, getUserWithRoleAndPermissions
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 1  # 1 hour
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
# should be kept secret
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "12345_54321")

JWT_REFRESH_SECRET_KEY = os.getenv(
    "JWT_REFRESH_SECRET_KEY", "Refresh12345_54321Refresh")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = get_logger()


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_jwt_token(payload: dict, expires_delta: int) -> dict:

    exp_time = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode = {"exp": exp_time, "sub": str(payload)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return dict(token=encoded_jwt, expire=expires_delta)


def generate_token(user: UserLogin, db: Session) -> dict:
    logger.info(f'token api call for  {user.email}')
    dbUser = getUserWithRoleAndPermissions([User.email == user.email], db)
    logger.info(f'user found {dbUser.email}')
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


def validateTokenAndReturnCurrentUser(token, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_payload = payload.get('sub')
        data_tuple = eval(user_payload)
        filter = [User.id == data_tuple[2]]
        current_user = getUserWithRoleAndPermissions(filter, db)
        return current_user
    except Exception as e:
        logger.info(e)
        raise e


def validate_token(request, db: Session):
    authorization_token = request.headers.get("Authorization")
    logger.info(f'token {authorization_token}')
    if authorization_token.startswith("Bearer "):
        token = authorization_token[len("Bearer "):]
        current_user = validateTokenAndReturnCurrentUser(token, db)
        request.state.current_user = current_user
        logger.info(
            f'token validated and current user is ${current_user}')
    else:
        # Raise an exception if the token does not start with "Bearer "
        raise HTTPException(
            status_code=400, detail=f"Invalid token")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def genreate_user(user: UserCreateWithRole, logger: Logger, db: Session) -> dict:
    user.password = get_hashed_password(user.password)
    return create_new_user(user, db, logger)


def isAuthenticated(request, currentUser):
    permissions_dict = {
        permission.url: permission.name
        for role in currentUser.roles
        for permission in role.permissions
    }
    logger.info(f'user all permissions {permissions_dict}')
    # it will check METHOD:API_PATH or * for super admin permission
    return permissions_dict.get(
        request.method+":"+request.url.path, None) or permissions_dict.get("*", None)
