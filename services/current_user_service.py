
from fastapi import Request


async def get_current_user(request: Request):
    hasCurrentUser = hasattr(request.state, 'current_user')
    print('attribute ', hasCurrentUser)
    if hasCurrentUser:
        print("authentication ", request.state.current_user)
        return request.state.current_user
    return None
