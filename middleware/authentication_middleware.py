from asyncio.log import logger
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status, HTTPException
import os
from fastapi.responses import JSONResponse

from custom_logger import get_logger
from services.auth_service import isAuthenticated
EXCLUDED_PATHS_FOR_AUTHENTICATION = os.getenv(
    "EXCLUDED_PATHS_FOR_AUTHENTICATION", ["/auth/token", "/auth/register", "/docs"])

logger = get_logger()


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(
            f'AuthenticationMiddleware called {request.url.path} {request.method}')

        if request.url.path not in EXCLUDED_PATHS_FOR_AUTHENTICATION:
            try:
                logger.info('checking current user')
                hasCurrentUser = hasattr(request.state, 'current_user')
                logger.info(f'attribute {hasCurrentUser}')
                if hasCurrentUser:
                    logger.info(f'authentication {request.state.current_user}')
                    currentUser = request.state.current_user
                    isRouteAllowed = isAuthenticated(request, currentUser)
                    logger.info(f'route allowed {isRouteAllowed}')
                    if not isRouteAllowed:
                        return JSONResponse(status_code=401, content={'message': "Permission denied"})

            except Exception as e:
                logger.info(e)
                return JSONResponse(status_code=401, content={'message': str(e)})
        response = await call_next(request)
        return response
