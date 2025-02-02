from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from .errors import CipherError


def configure_encryption_exceptions(app: FastAPI) -> None:
    @app.exception_handler(CipherError)
    async def cipher_security_exception_handler(
        request: Request, exc: CipherError
    ) -> Response:
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
            ),
        )
