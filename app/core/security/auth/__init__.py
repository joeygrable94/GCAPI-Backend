from typing import List

from app.core.config import settings

from .auth0 import (
    Auth0,
    Auth0HTTPBearer,
    Auth0User,
    JwksDict,
    JwksKeyDict,
    OAuth2ImplicitBearer,
)
from .exceptions import (
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
    HTTPAuth0Error,
)
from .roles import UserRole

auth = Auth0(
    domain=settings.auth.domain,
    api_audience=settings.auth.audience,
    scopes=settings.auth.scopes,
)


__all__: List[str] = [
    "Auth0",
    "Auth0HTTPBearer",
    "Auth0UnauthenticatedException",
    "Auth0UnauthorizedException",
    "Auth0User",
    "HTTPAuth0Error",
    "JwksDict",
    "JwksKeyDict",
    "OAuth2ImplicitBearer",
    "auth",
    "UserRole",
]
