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
    configure_authorization_exceptions,
)
from .csrf import CsrfProtect, CsrfProtectError, CsrfSettings, configure_csrf_exceptions
from .encryption import (
    CipherError,
    DecryptionError,
    EncryptionError,
    SecureMessage,
    SignatureVerificationError,
    configure_encryption_exceptions,
    load_api_keys,
)
from .permissions import (
    AuthPermissionException,
    configure_permissions,
    configure_permissions_exceptions,
    has_permission,
    list_permissions,
)
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
    "configure_authorization_exceptions",
    "configure_csrf_exceptions",
    "configure_encryption_exceptions",
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
    "configure_permissions_exceptions",
    "configure_permissions",
    "has_permission",
    "list_permissions",
]
