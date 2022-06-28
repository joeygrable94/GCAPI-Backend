from typing import Any, List, Type

from pydantic import UUID4

from app.db.repositories.base import BaseRepository
from app.db.schemas import ItemCreate, ItemRead, ItemUpdate
from app.db.tables import Item

from .base import PER_PAGE_MAX_COUNT, sql_select


class ItemsRepository(BaseRepository[ItemCreate, ItemRead, ItemUpdate, Item]):
    @property
    def _schema_create(self) -> Type[ItemCreate]:
        return ItemCreate

    @property
    def _schema_read(self) -> Type[ItemRead]:
        return ItemRead

    @property
    def _schema_update(self) -> Type[ItemUpdate]:
        return ItemUpdate

    @property
    def _table(self) -> Type[Item]:
        return Item

    async def _list_by_user(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT, user_id: UUID4 = None
    ) -> List[ItemRead]:
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

    async def list(self, page: int = 1, user_id: UUID4 = None) -> List[ItemRead]:
        skip, limit = self.paginate(page)
        if user_id:
            return await self._list_by_user(skip=skip, limit=limit, user_id=user_id)
        else:
            return await self._list(skip=skip, limit=limit)
