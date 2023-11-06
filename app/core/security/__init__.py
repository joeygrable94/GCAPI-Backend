from typing import List

from .auth import (
    Auth0,
    Auth0HTTPBearer,
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
    Auth0User,
    HTTPAuth0Error,
    JwksDict,
    JwksKeyDict,
    OAuth2ImplicitBearer,
    auth,
)
from .csrf import CsrfProtect, CsrfProtectError, CsrfSettings
from .encryption import (
    CipherError,
    DecryptionError,
    EncryptionError,
    SecureMessage,
    SignatureVerificationError,
    load_api_keys,
)
from .permissions import (
    AuthPermissionException,
    configure_permissions,
    has_permission,
    list_permissions,
)
from .rate_limiter import FastAPILimiter, RateLimitedRequestException, RateLimiter
from .schemas import CsrfToken, EncryptedMessage, PlainMessage, RateLimitedToken

__all__: List[str] = [
    "EncryptionError",
    "DecryptionError",
    "auth",
    "Auth0",
    "Auth0HTTPBearer",
    "Auth0UnauthenticatedException",
    "Auth0UnauthorizedException",
    "Auth0User",
    "CipherError",
    "CsrfProtect",
    "CsrfProtectError",
    "CsrfSettings",
    "CsrfToken",
    "EncryptedMessage",
    "PlainMessage",
    "RateLimitedToken",
    "HTTPAuth0Error",
    "JwksDict",
    "JwksKeyDict",
    "OAuth2ImplicitBearer",
    "load_api_keys",
    "SecureMessage",
    "SignatureVerificationError",
    "AuthPermissionException",
    "configure_permissions",
    "has_permission",
    "list_permissions",
    "FastAPILimiter",
    "RateLimiter",
    "RateLimitedRequestException",
]
