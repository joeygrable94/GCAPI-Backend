from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel


class AuthUnauthenticatedException(HTTPException):
    def __init__(self, detail: str, **kwargs: Any) -> None:
        """Returns HTTP 401"""
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, **kwargs)


class AuthUnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs: Any) -> None:
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail, **kwargs)


class HTTPAuthError(BaseModel):
    detail: str


def configure_authorization_exceptions(app: FastAPI) -> None:
    @app.exception_handler(AuthUnauthenticatedException)
    async def auth0_unauthenticated_exception_handler(
        request: Request, exc: AuthUnauthenticatedException
    ) -> Response:
        request_headers: dict[str, str] = {}
        if exc.headers is not None:
            request_headers.update(exc.headers)  # pragma: no cover
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.detail,
                headers=request_headers,
            ),
        )

    @app.exception_handler(AuthUnauthorizedException)
    async def auth0_unauthorized_exception_handler(
        request: Request, exc: AuthUnauthorizedException
    ) -> Response:
        request_headers: dict[str, str] = {}
        if exc.headers is not None:
            request_headers.update(exc.headers)
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.detail,
                headers=request_headers,
            ),
        )
