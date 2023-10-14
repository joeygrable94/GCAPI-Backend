from typing import Any

from fastapi import HTTPException, status
from pydantic import BaseModel


class Auth0UnauthenticatedException(HTTPException):
    def __init__(self, detail: str, **kwargs: Any) -> None:
        """Returns HTTP 401"""
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, **kwargs)


class Auth0UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs: Any) -> None:
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail, **kwargs)


class HTTPAuth0Error(BaseModel):
    detail: str
