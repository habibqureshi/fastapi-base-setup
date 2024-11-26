
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from custom_logger import get_logger
from database import get_db
from fastapi.responses import JSONResponse
from jose import jwt
import os
from fastapi.responses import JSONResponse
from database import get_db
from models.user_model import User
from services.user_service import getUserWithRoleAndPermissions

EXCLUDED_PATHS_FOR_AUTHENTICATION = os.getenv(
    "EXCLUDED_PATHS_FOR_AUTHENTICATION", ["/auth/token", "/auth/register"])
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "12345_54321")
ALGORITHM = "HS256"

logger = get_logger()


def validated_token(token, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_payload = payload.get('sub')
        data_tuple = eval(user_payload)
        filer = [User.id == data_tuple[2]]

        current_user = getUserWithRoleAndPermissions(filer, db)
        return current_user
    except Exception as e:
        logger.info(e)
        raise e


class AuthorizationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        logger.info("AuthorizationMiddleware called")
        if request.url.path not in EXCLUDED_PATHS_FOR_AUTHENTICATION:
            try:
                authorization_token = request.headers.get("Authorization")
                logger.info(f'token {authorization_token}')
                if authorization_token.startswith("Bearer "):
                    token = authorization_token[len("Bearer "):]
                    db = get_db()
                    session = next(db)
                    current_user = validated_token(token, session)
                    request.state.current_user = current_user
                    logger.info(
                        f'token validated and current user is ${current_user}')
                else:
                    # Raise an exception if the token does not start with "Bearer "
                    return JSONResponse(status_code=401, content={'message': "Invalid token"})
            except Exception as e:
                logger.info(e)
                return JSONResponse(status_code=401, content={'message': str(e)})
        else:
            logger.info("open endpoint")
        # If authentication is valid or excluded, continue to the next middleware or endpoint
        response = await call_next(request)
        return response
