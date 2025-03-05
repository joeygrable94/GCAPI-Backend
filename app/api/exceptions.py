from fastapi import FastAPI

from app.entities.api.exceptions import configure_api_exceptions
from app.entities.core_organization.exceptions import configure_organization_exceptions
from app.entities.core_user.exceptions import configure_user_exceptions
from app.entities.website.exceptions import configure_website_exceptions
from app.services.clerk import configure_clerk_authorization_exceptions
from app.services.csrf import configure_csrf_exceptions
from app.services.encryption import configure_encryption_exceptions
from app.services.permission import configure_permissions_exceptions


def configure_exceptions(app: FastAPI) -> None:
    configure_api_exceptions(app)
    configure_user_exceptions(app)
    configure_organization_exceptions(app)
    configure_website_exceptions(app)
    configure_permissions_exceptions(app)
    configure_clerk_authorization_exceptions(app)
    configure_csrf_exceptions(app)
    configure_encryption_exceptions(app)
