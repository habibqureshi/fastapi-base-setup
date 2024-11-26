

from asyncio.log import logger
from re import M

from fastapi import FastAPI, Depends, Request

from middleware.authentication_middleware import AuthenticationMiddleware
from middleware.authorization_middleware import AuthorizationMiddleware
from routers import user_router, auth_router
from database import engine, get_db, Base
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from services.user_service import getUserById

Base.metadata.create_all(bind=engine)







# log = logging.getLog/ger(__name__)

app = FastAPI()
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(AuthorizationMiddleware)
app.include_router(user_router.router)
app.include_router(auth_router.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": [
                {"field": error["loc"][1], "message": error["msg"]} for error in exc.errors()
            ],
        },
    )
