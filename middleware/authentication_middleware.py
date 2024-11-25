from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status, HTTPException
import os
from fastapi.responses import JSONResponse
EXCLUDED_PATHS_FOR_AUTHENTICATION = os.getenv(
    "EXCLUDED_PATHS_FOR_AUTHENTICATION", ["/auth/token", "/auth/register"])


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("AuthenticationMiddleware called",
              request.url.path, request.method)

        if request.url.path not in EXCLUDED_PATHS_FOR_AUTHENTICATION:
            try:
                print('checking current user')
                hasCurrentUser = hasattr(request.state, 'current_user')
                print('attribute ', hasCurrentUser)
                if hasCurrentUser:
                    print("authentication ", request.state.current_user)
                    currentUser = request.state.current_user

                    permissions_dict = {
                        permission.url: permission.name
                        for role in currentUser.roles
                        for permission in role.permissions
                    }
                    print("user all permissions", permissions_dict)
                    print("have permission")
                    # it will check METHOD:API_PATH or * for super admin permission
                    isRouteAllowed = permissions_dict.get(
                        request.method+":"+request.url.path, None)
                    # or permissions_dict.get("*", None)
                    if not isRouteAllowed:
                        return JSONResponse(status_code=401, content={'message': "Permission denied"})

            except Exception as e:
                print(e)
                return JSONResponse(status_code=401, content={'message': str(e)})
        response = await call_next(request)
        return response
