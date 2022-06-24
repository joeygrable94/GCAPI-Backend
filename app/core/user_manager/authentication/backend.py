from typing import Any, Generic

from fastapi import Response

from app.core.user_manager.types import UP, ID
from app.core.user_manager.authentication.strategy import (
    Strategy,
    StrategyDestroyNotSupportedError,
)
from app.core.user_manager.authentication.transport import (
    Transport,
    TransportLogoutNotSupportedError,
)
from app.core.user_manager.types import DependencyCallable


class AuthenticationBackend(Generic[UP, ID]):
    """
    Combination of an authentication transport and strategy.

    Together, they provide a full authentication method logic.

    :param name: Name of the backend.
    :param transport: Authentication transport instance.
    :param get_strategy: Dependency callable returning
    an authentication strategy instance.
    """

    name: str
    transport: Transport

    def __init__(
        self,
        name: str,
        transport: Transport,
        get_strategy: DependencyCallable[Strategy[UP, ID]],
    ):
        self.name = name
        self.transport = transport
        self.get_strategy = get_strategy

    async def login(
        self,
        strategy: Strategy[UP, ID],
        user: UP,
        response: Response,
    ) -> Any:
        token = await strategy.write_token(user)
        return await self.transport.get_login_response(token, response)

    async def logout(
        self,
        strategy: Strategy[UP, ID],
        user: UP,
        token: str,
        response: Response,
    ) -> Any:
        try:
            await strategy.destroy_token(token, user)
        except StrategyDestroyNotSupportedError:
            pass

        try:
            await self.transport.get_logout_response(response)
        except TransportLogoutNotSupportedError:
            return None
