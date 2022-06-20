from typing import Any, Protocol  # pragma: no cover

from fastapi import Response
from fastapi.security.base import SecurityBase


class TransportLogoutNotSupportedError(Exception):
    pass


class Transport(Protocol):
    scheme: SecurityBase

    async def get_login_response(self, token: str, response: Response) -> Any:
        ...  # pragma: no cover

    async def get_logout_response(self, response: Response) -> Any:
        ...  # pragma: no cover
