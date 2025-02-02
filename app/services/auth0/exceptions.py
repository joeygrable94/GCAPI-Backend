from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from .errors import AuthUnauthenticatedException, AuthUnauthorizedException


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
