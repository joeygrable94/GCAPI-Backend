from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from .errors import AuthPermissionException


def configure_permissions_exceptions(app: FastAPI) -> None:
    @app.exception_handler(AuthPermissionException)
    async def permissions_exception_handler(
        request: Request, exc: AuthPermissionException
    ) -> Response:
        request_headers = {}
        if exc.headers:
            request_headers.update(exc.headers)
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers=request_headers,
            ),
        )
