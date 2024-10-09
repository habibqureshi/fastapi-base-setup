import logging
from asyncio.log import logger
from re import M
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from typing import Union
from routers import userRouter
from database import engine, get_db, Base
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

Base.metadata.create_all(bind=engine)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# log = logging.getLogger(__name__)


app = FastAPI()
app.include_router(userRouter.router)


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


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


@app.get('/')
def get():
    return {"status": "ok"}


@app.post('/')
def post(item: Item):
    logger.debug("hi", item)
    # log.info(item)
    return {"status": "oki", "data": item}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
