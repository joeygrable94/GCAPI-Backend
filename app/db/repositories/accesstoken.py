from typing import Any, Optional, Type

from sqlalchemy import func, select

from app.db.repositories.base import BaseRepository
from app.db.schemas import AccessTokenCreate, AccessTokenRead, AccessTokenUpdate
from app.db.tables import AccessToken


class AccessTokensRepository(
    BaseRepository[
        AccessTokenCreate,
        AccessTokenRead,
        AccessTokenUpdate,
        AccessToken,
    ]
):
    @property
    def _table(self) -> Type[AccessToken]:  # type: ignore
        return AccessToken

    async def read_by_token(self, token_jti: str) -> Optional[AccessToken]:
        query: Any = select(self._table).where(  # type: ignore
            func.lower(self._table.token_jti) == func.lower(token_jti)
        )
        return await self._get(query)
