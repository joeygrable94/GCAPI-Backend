from asgi_correlation_id.context import correlation_id
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler


class CsrfProtectError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class InvalidHeaderError(CsrfProtectError):
    def __init__(self, message: str):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, message)


class MissingTokenError(CsrfProtectError):
    def __init__(self, message: str):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class TokenValidationError(CsrfProtectError):
    def __init__(self, message: str):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


def configure_csrf_exceptions(app: FastAPI) -> None:

    @app.exception_handler(CsrfProtectError)
    async def csrf_protect_exception_handler(
        request: Request, exc: CsrfProtectError
    ) -> Response:  # noqa: E501
        request_headers = {
            "x-request-id": correlation_id.get() or "",
            "Access-Control-Expose-Headers": "x-request-id",
        }
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
                headers=request_headers,
            ),
        )
