from .controller import ClerkAuth, ClerkHTTPBearer
from .errors import ClerkUnauthenticatedException, ClerkUnauthorizedException
from .exceptions import configure_clerk_authorization_exceptions
from .schemas import ClerkUser
from .settings import ClerkSettings, clerk_settings, get_clerk_settings

clerk_controller = ClerkAuth(
    secret_key=clerk_settings.secret_key,
    jwks_url=clerk_settings.jwks_url,
    issuer=clerk_settings.issuer,
    pem_public_key=clerk_settings.pem_public_key,
)

__all__: list[str] = [
    "ClerkAuth",
    "ClerkHTTPBearer",
    "ClerkUnauthenticatedException",
    "ClerkUnauthorizedException",
    "configure_clerk_authorization_exceptions",
    "ClerkUser",
    "ClerkSettings",
    "clerk_settings",
    "get_clerk_settings",
]
