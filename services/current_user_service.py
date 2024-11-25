
from fastapi import Request


async def get_current_user(request: Request):
    return request.state.current_user
