from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler

from app.api.exceptions.errors import ErrorCode


class AuthPermissionException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        message: str = ErrorCode.INSUFFICIENT_PERMISSIONS,
    ):
        self.status_code = status_code
        self.message = message
        self.headers = {"WWW-Authenticate": "Bearer"}


def configure_permissions_exceptions(app: FastAPI) -> None:

    @app.exception_handler(AuthPermissionException)
    async def permissions_exception_handler(
        request: Request, exc: AuthPermissionException
    ) -> Response:  # noqa: E501
        request_headers = {
            "x-request-id": correlation_id.get() or "",
            "Access-Control-Expose-Headers": "x-request-id",
        }
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
