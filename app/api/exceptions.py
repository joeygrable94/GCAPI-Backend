from fastapi import FastAPI

from app.entities.api.exceptions import configure_api_exceptions
from app.entities.client.exceptions import configure_client_exceptions
from app.entities.user.exceptions import configure_user_exceptions
from app.entities.website.exceptions import configure_website_exceptions
from app.services.auth0 import configure_authorization_exceptions
from app.services.csrf import configure_csrf_exceptions
from app.services.encryption import configure_encryption_exceptions
from app.services.permission import configure_permissions_exceptions


def configure_exceptions(app: FastAPI) -> None:
    configure_api_exceptions(app)
    configure_user_exceptions(app)
    configure_client_exceptions(app)
    configure_website_exceptions(app)
    configure_permissions_exceptions(app)
    configure_authorization_exceptions(app)
    configure_csrf_exceptions(app)
    configure_encryption_exceptions(app)
