from enum import Enum
from typing import Dict, Union

from pydantic import BaseModel


class ErrorModel(BaseModel):
    detail: Union[str, Dict[str, str]]


class ErrorCodeReasonModel(BaseModel):
    code: str
    reason: str


class ErrorCode(str, Enum):
    # auth
    USER_FORBIDDEN = "USER_FORBIDDEN"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_ALREADY_VERIFIED = "USER_ALREADY_VERIFIED"
    # user
    USER_PASSWORD_INVALID = "USER_PASSWORD_INVALID"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_NOT_ACTIVE = "USER_NOT_ACTIVE"
    USER_NOT_VERIFIED = "USER_NOT_VERIFIED"
    # tokens
    BAD_CREDENTIALS = "BAD_CREDENTIALS"
    BAD_TOKEN = "BAD_TOKEN"
    TOKEN_MISSING = "TOKEN_MISSING"
    TOKEN_INVALID = "TOKEN_INVALID"
    TOKEN_REVOKED = "TOKEN_REVOKED"
    FRESH_TOKEN_REQUIRED = "FRESH_TOKEN_REQUIRED"
    ACCESS_TOKEN_REQUIRED = "ACCESS_TOKEN_REQUIRED"
    REFRESH_TOKEN_REQUIRED = "REFRESH_TOKEN_REQUIRED"
    TOKEN_CSRF_INVALID = "TOKEN_CSRF_INVALID"
