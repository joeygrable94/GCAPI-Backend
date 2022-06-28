from typing import Any, List, Type

from pydantic import UUID4

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientCreate, ClientRead, ClientUpdate
from app.db.tables import Client

from .base import PER_PAGE_MAX_COUNT, sql_select


class ClientsRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _schema_create(self) -> Type[ClientCreate]:
        return ClientCreate

    @property
    def _schema_read(self) -> Type[ClientRead]:
        return ClientRead

    @property
    def _schema_update(self) -> Type[ClientUpdate]:
        return ClientUpdate

    @property
    def _table(self) -> Type[Client]:
        return Client

    async def _list_by_user(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT, user_id: UUID4 = None
    ) -> List[ClientRead]:
        if not user_id:
            return list()
        query: Any = (
            sql_select(self._table)
            .where(self._table.user_id == user_id)
            .offset(skip)
            .limit(limit)  # type: ignore
        )
        result: Any = await self._db.execute(query)
        data: Any = result.scalars().all()
        return list(data)

    async def list(self, page: int = 1, user_id: UUID4 = None) -> List[ClientRead]:
        skip, limit = self.paginate(page)
        if user_id:
            return await self._list_by_user(skip=skip, limit=limit, user_id=user_id)
        else:
            return await self._list(skip=skip, limit=limit)
