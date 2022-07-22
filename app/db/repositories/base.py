import abc
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import UUID4
from sqlalchemy import select as sql_select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utilities import paginate
from app.db.schemas.base import BaseSchema
from app.db.tables.base import TableBase
from app.db.utilities import _get_uuid

SCHEMA_CREATE = TypeVar("SCHEMA_CREATE", bound=BaseSchema)
SCHEMA_READ = TypeVar("SCHEMA_READ", bound=BaseSchema)
SCHEMA_UPDATE = TypeVar("SCHEMA_UPDATE", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=TableBase)
PER_PAGE_MAX_COUNT: int = 100


class BaseRepository(
    Generic[SCHEMA_CREATE, SCHEMA_READ, SCHEMA_UPDATE, TABLE], metaclass=abc.ABCMeta
):
    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session

    @property
    @abc.abstractmethod
    def _schema_read(self) -> Any:
        pass

    @property
    @abc.abstractmethod
    def _table(self) -> Any:
        pass

    @staticmethod
    def generate_uuid() -> Any:
        return lambda: str(_get_uuid())

    def _preprocess_create(self, values: Dict) -> Dict:
        if "id" not in values:
            values["id"] = self.generate_uuid()
        return values

    async def _get(self, query: Any) -> Optional[Any]:
        results: Any = await self._db.execute(query)
        data: Any = results.first()
        if data is None:
            return None
        return data[0]

    async def _list(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT
    ) -> Optional[Union[List[SCHEMA_READ], List]]:
        query: Any = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: Any = result.scalars().all()
        return data

    async def list(self, page: int = 1) -> Optional[Union[List[SCHEMA_READ], List]]:
        skip, limit = paginate(page)
        return await self._list(skip=skip, limit=limit)

    async def create(self, schema: Union[SCHEMA_CREATE, Any]) -> SCHEMA_READ:
        entry: Any = self._table(id=self.generate_uuid(), **schema.dict())
        self._db.add(entry)
        await self._db.commit()
        return self._schema_read.from_orm(entry)

    async def read(self, entry_id: UUID4) -> Optional[SCHEMA_READ]:
        query: Any = sql_select(self._table).where(  # type: ignore
            self._table.id == entry_id
        )
        entry: Any = await self._get(query)
        if not entry:
            return None
        return self._schema_read.from_orm(entry)

    async def update(
        self, entry_id: UUID4, schema: Union[SCHEMA_UPDATE, Any]
    ) -> Optional[SCHEMA_READ]:
        query: Any = sql_select(self._table).where(  # type: ignore
            self._table.id == entry_id
        )
        entry: Any = await self._get(query)
        if not entry:
            return None
        for k, v in schema.dict(exclude_unset=True).items():
            setattr(entry, k, v)
        await self._db.commit()
        await self._db.refresh(entry)
        return self._schema_read.from_orm(entry)

    async def delete(self, entry_id: UUID4) -> Optional[SCHEMA_READ]:
        query: Any = sql_select(self._table).where(  # type: ignore
            self._table.id == entry_id
        )
        entry: Any = await self._get(query)
        if not entry:
            return None
        await self._db.delete(entry)
        await self._db.commit()
        return self._schema_read.from_orm(entry)
