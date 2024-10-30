from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler


class CipherError(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Cipher encryption Error",
    ):
        self.status_code = status_code
        self.message = message


class SignatureVerificationError(CipherError):
    def __init__(self, message: str = "encryption signature not valid"):
        super().__init__(message=message)


class EncryptionError(CipherError):
    def __init__(self, message: str = "error encrypting message"):
        super().__init__(message=message)


class DecryptionError(CipherError):
    def __init__(self, message: str = "error decrypting message"):
        super().__init__(message=message)


def configure_encryption_exceptions(app: FastAPI) -> None:

    @app.exception_handler(CipherError)
    async def cipher_security_exception_handler(
        request: Request, exc: CipherError
    ) -> Response:  # noqa: E501
        return await http_exception_handler(  # pragma: no cover
            request,
            HTTPException(
                exc.status_code,
                detail=exc.message,
            ),
        )
