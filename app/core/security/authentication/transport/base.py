from typing import Any  # pragma: no cover
from typing import Protocol

from fastapi import Response
from fastapi.security.base import SecurityBase

from app.api.openapi import OpenAPIResponseType


class TransportLogoutNotSupportedError(Exception):
    pass


class Transport(Protocol):
    scheme: SecurityBase

    async def get_login_response(self, token: str, response: Response) -> Any:
        ...  # pragma: no cover

    async def get_logout_response(self, response: Response) -> Any:
        ...  # pragma: no cover

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        """Return a dictionary to use for the openapi responses route parameter."""
        ...  # pragma: no cover

    @staticmethod
    def get_openapi_logout_responses_success() -> OpenAPIResponseType:
        """Return a dictionary to use for the openapi responses route parameter."""
        ...  # pragma: no cover
