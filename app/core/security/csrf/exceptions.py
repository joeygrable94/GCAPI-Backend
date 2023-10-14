from fastapi import status


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
