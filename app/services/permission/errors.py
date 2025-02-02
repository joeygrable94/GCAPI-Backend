from fastapi import status

from .constants import ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS


class AuthPermissionException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        message: str = ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS,
    ):
        self.status_code = status_code
        self.message = message
        self.headers = {"WWW-Authenticate": "Bearer"}
