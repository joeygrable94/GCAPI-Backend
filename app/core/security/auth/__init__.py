from typing import List

from app.core.config import settings

from .auth0 import (
    Auth0,
    Auth0HTTPBearer,
    AuthUser,
    JwksDict,
    JwksKeyDict,
    OAuth2ImplicitBearer,
)
from .exceptions import (
    AuthUnauthenticatedException,
    AuthUnauthorizedException,
    HTTPAuthError,
    configure_authorization_exceptions,
)

auth = Auth0(
    domain=settings.auth.domain,
    api_audience=settings.auth.audience,
    scopes={
        "permission:test": "Grant GCAPI Permission to test the API using your email credentials."
    },
)


__all__: List[str] = [
    "Auth0",
    "Auth0HTTPBearer",
    "AuthUnauthenticatedException",
    "AuthUnauthorizedException",
    "AuthUser",
    "configure_authorization_exceptions",
    "HTTPAuthError",
    "JwksDict",
    "JwksKeyDict",
    "OAuth2ImplicitBearer",
    "auth",
]
