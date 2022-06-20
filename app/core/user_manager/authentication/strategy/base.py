from typing import Generic, Optional, Protocol  # pragma: no cover

from app.core.user_manager.models import UP, ID
from app.core.user_manager.manager import UserManager


class StrategyDestroyNotSupportedError(Exception):
    pass


class Strategy(Protocol, Generic[UP, ID]):
    async def read_token(
        self, token: Optional[str], user_manager: UserManager[UP, ID]
    ) -> Optional[UP]:
        ...  # pragma: no cover

    async def write_token(self, user: UP) -> str:
        ...  # pragma: no cover

    async def destroy_token(self, token: str, user: UP) -> None:
        ...  # pragma: no cover
