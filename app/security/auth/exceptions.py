from typing import Any


class AuthException(Exception):
    """
    Base except which all fastapi_another_jwt_auth errors extend
    """

    def __init__(
        self,
        reason: Any,
    ) -> None:
        self.reason: Any = reason  # pragma: no cover


class CSRFError(AuthException):
    """
    An error with CSRF protection
    """


class MissingTokenError(AuthException):
    """
    Error raised when token not found
    """


class ExpiredTokenError(AuthException):
    """
    Error raised when a token is used after the
    date at which that tokens accesss expires
    """


class RevokedTokenError(AuthException):
    """
    Error raised when a revoked token attempt to access a protected endpoint
    """


class AccessTokenRequired(AuthException):
    """
    Error raised when a valid, non-access JWT attempt to access an endpoint
    protected by jwt_required, jwt_optional, fresh_jwt_required
    """


class RefreshTokenRequired(AuthException):
    """
    Error raised when a valid, non-refresh JWT attempt to access an endpoint
    protected by jwt_refresh_token_required
    """


class FreshTokenRequired(AuthException):
    """
    Error raised when a valid, non-fresh JWT attempt to access an endpoint
    protected by fresh_jwt_required
    """
