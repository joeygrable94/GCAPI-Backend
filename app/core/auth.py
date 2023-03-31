from fastapi_auth0 import Auth0

from app.core.config import settings

auth = Auth0(
    domain=settings.AUTH0_DOMAIN,
    api_audience=settings.AUTH0_API_AUDIENCE,
    scopes=settings.BASE_PRINCIPALS,
)
