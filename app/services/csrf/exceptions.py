from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from .errors import CsrfProtectError


def configure_csrf_exceptions(app: FastAPI) -> None:
    @app.exception_handler(CsrfProtectError)
    async def csrf_protect_exception_handler(
        request: Request, exc: CsrfProtectError
    ) -> Response:
        return await http_exception_handler(
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
            ),
        )
