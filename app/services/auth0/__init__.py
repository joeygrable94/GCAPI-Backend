from typing import List

from .controller import Auth0, Auth0HTTPBearer, OAuth2ImplicitBearer
from .errors import (
    AuthUnauthenticatedException,
    AuthUnauthorizedException,
    HTTPAuthError,
)
from .exceptions import configure_authorization_exceptions
from .schemas import AuthUser, JwksDict, JwksKeyDict
from .settings import AuthSettings, auth_settings, get_auth_settings

auth_controller = Auth0(
    domain=auth_settings.domain,
    api_audience=auth_settings.audience,
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
    "auth_controller",
    "auth_settings",
    "AuthSettings",
    "get_auth_settings",
]
