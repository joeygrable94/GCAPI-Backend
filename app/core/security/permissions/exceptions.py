from fastapi import status

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
