from datetime import datetime
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
    def _schema_read(self) -> Type[AccessTokenRead]:  # type: ignore
        return AccessTokenRead

    @property
    def _table(self) -> Type[AccessToken]:  # type: ignore
        return AccessToken

    async def read_by_token(
        self, token: str, max_age: Optional[datetime] = None
    ) -> Optional[AccessToken]:
        query: Any = select(self._table).where(  # type: ignore
            func.lower(self._table.token) == func.lower(token)
        )
        if max_age is not None:
            query = query.where(self._table.created_on >= max_age)
            print(query)
        return await self._get(query)
