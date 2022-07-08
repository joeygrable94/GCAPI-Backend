from typing import Generic  # pragma: no cover
from typing import Optional, Protocol

from app.core.security.manager import UserManager
from app.db.schemas.user import ID, UP


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
