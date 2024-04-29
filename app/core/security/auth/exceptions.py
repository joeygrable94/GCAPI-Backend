from typing import Any

from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from pydantic import BaseModel


class Auth0UnauthenticatedException(HTTPException):
    def __init__(self, detail: str, **kwargs: Any) -> None:
        """Returns HTTP 401"""
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, **kwargs)


class Auth0UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs: Any) -> None:
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail, **kwargs)


class HTTPAuth0Error(BaseModel):
    detail: str


def configure_authorization_exceptions(app: FastAPI) -> None:

    @app.exception_handler(Auth0UnauthenticatedException)
    async def auth0_unauthenticated_exception_handler(
        request: Request, exc: Auth0UnauthenticatedException
    ) -> Response:  # noqa: E501
        request_headers = {
            "x-request-id": correlation_id.get() or "",
            "Access-Control-Expose-Headers": "x-request-id",
        }
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

    @app.exception_handler(Auth0UnauthorizedException)
    async def auth0_unauthorized_exception_handler(
        request: Request, exc: Auth0UnauthorizedException
    ) -> Response:  # noqa: E501
        request_headers = {
            "x-request-id": correlation_id.get() or "",
            "Access-Control-Expose-Headers": "x-request-id",
        }
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
