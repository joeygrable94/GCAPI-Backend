from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from .errors import ClerkUnauthenticatedException, ClerkUnauthorizedException


def configure_clerk_authorization_exceptions(app: FastAPI) -> None:
    @app.exception_handler(ClerkUnauthenticatedException)
    async def clerk_unauthenticated_exception_handler(
        request: Request, exc: ClerkUnauthenticatedException
    ) -> Response:  # pragma: no cover
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

    @app.exception_handler(ClerkUnauthorizedException)
    async def clerk_unauthorized_exception_handler(
        request: Request, exc: ClerkUnauthorizedException
    ) -> Response:  # pragma: no cover
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
