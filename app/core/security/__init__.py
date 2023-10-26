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
from .csrf import CsrfProtect, CsrfProtectError
from .encryption import (
    AESCipherCBC,
    AESDecryptionError,
    AESEncryptionError,
    CipherError,
    RSACipher,
    RSADecryptionError,
    RSAEncryptionError,
    load_api_keys,
)
from .permissions import (
    AuthPermissionException,
    configure_permissions,
    has_permission,
    list_permissions,
)
from .rate_limiter import (
    FastAPILimiter,
    RateLimitedRequestException,
    RateLimiter,
    WebSocketRateLimiter,
)
from .schemas import (
    CsrfToken,
    EncryptedMessage,
    PlainMessage,
    RateLimitedToken,
    RSADecryptMessage,
    RSAEncryptMessage,
)

__all__: List[str] = [
    "AESCipherCBC",
    "AESEncryptionError",
    "AESDecryptionError",
    "auth",
    "Auth0",
    "Auth0HTTPBearer",
    "Auth0UnauthenticatedException",
    "Auth0UnauthorizedException",
    "Auth0User",
    "CipherError",
    "CsrfProtect",
    "CsrfProtectError",
    "CsrfToken",
    "EncryptedMessage",
    "PlainMessage",
    "RateLimitedToken",
    "RSADecryptMessage",
    "RSAEncryptMessage",
    "HTTPAuth0Error",
    "JwksDict",
    "JwksKeyDict",
    "OAuth2ImplicitBearer",
    "RSACipher",
    "load_api_keys",
    "RSACipherError",
    "RSAEncryptionError",
    "RSADecryptionError",
    "AuthPermissionException",
    "configure_permissions",
    "has_permission",
    "list_permissions",
    "FastAPILimiter",
    "RateLimiter",
    "WebSocketRateLimiter",
    "RateLimitedRequestException",
]
