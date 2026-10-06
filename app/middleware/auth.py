from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.responses import JSONResponse

from app.core.security import decode_access_token


PUBLIC_PATHS = {
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/auth/login",
    "/api/auth/register",
}


async def auth_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:

    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    token = request.cookies.get("access_token")

    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"},
        )

    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token expired"},
        )
    except InvalidTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid token"},
        )

    request.state.user_id = payload.get("user_id")

    return await call_next(request)
