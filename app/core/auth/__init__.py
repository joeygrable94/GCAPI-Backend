from app.core.config import settings

from .auth0 import (
    Auth0,
    Auth0HTTPBearer,
    Auth0UnauthenticatedException,
    Auth0UnauthorizedException,
    Auth0User,
    HTTPAuth0Error,
    JwksDict,
    JwksKeyDict,
    OAuth2ImplicitBearer,
)

auth = Auth0(
    domain=settings.AUTH0_DOMAIN,
    api_audience=settings.AUTH0_API_AUDIENCE,
    scopes=settings.BASE_PRINCIPALS,
)
