from fastapi import status


class AuthPermissionException(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        message: str = "Insufficient permissions",
    ):
        self.status_code = status_code
        self.message = message
        self.headers = {"WWW-Authenticate": "Bearer"}
