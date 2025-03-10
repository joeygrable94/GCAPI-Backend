import abc
from typing import Any, Generic, TypeVar, Union

from pydantic import UUID4
from sqlalchemy import Select, and_
from sqlalchemy import select as sql_select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema import BaseSchema
from app.db.base import Base
from app.utilities import get_uuid

SCHEMA_CREATE = TypeVar("SCHEMA_CREATE", bound=BaseSchema)
SCHEMA_READ = TypeVar("SCHEMA_READ", bound=BaseSchema)
SCHEMA_UPDATE = TypeVar("SCHEMA_UPDATE", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Base)


class BaseRepository(
    Generic[SCHEMA_CREATE, SCHEMA_READ, SCHEMA_UPDATE, TABLE],
    metaclass=abc.ABCMeta,
):
    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session

    @property
    @abc.abstractmethod
    def _table(self) -> Generic[TABLE]:  # pragma: no cover
        pass

    def gen_uuid(self) -> UUID4:
        return get_uuid()

    def _preprocess_create(self, values: dict) -> dict:  # pragma: no cover
        if "id" not in values:
            values["id"] = self.gen_uuid()
        return values

    async def _get(self, query: Any) -> TABLE | None:
        results: Any = await self._db.execute(query)
        data: Any = results.first()
        if data is None:
            return None
        return data[0]

    def query_list(self) -> Select:
        stmt = sql_select(self._table)
        return stmt

    async def create(self, schema: Union[SCHEMA_CREATE, Any]) -> TABLE:
        self._db.begin()
        entry: Any = self._table(id=self.gen_uuid(), **schema.model_dump())
        self._db.add(entry)
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def read_by(self, field_name: str, field_value: Any) -> TABLE | None:
        self._db.begin()
        check_val: Any = getattr(self._table, field_name)
        query: Any = sql_select(self._table).where(check_val == field_value)
        entry: Any = await self._get(query)
        if not entry:
            return None
        return entry

    async def read(self, entry_id: UUID4) -> TABLE | None:
        self._db.begin()
        query: Any = sql_select(self._table).where(self._table.id == entry_id)
        entry: Any = await self._get(query)
        if not entry:
            return None
        return entry

    async def update(
        self,
        entry: TABLE,
        schema: Union[SCHEMA_UPDATE, Any],
    ) -> TABLE:
        self._db.begin()
        for k, v in schema.model_dump(exclude_unset=True, exclude_none=True).items():
            setattr(entry, k, v)
        self._db.add(entry)
        await self._db.commit()
        await self._db.refresh(entry)  # pragma: no cover
        return entry  # pragma: no cover

    async def delete(self, entry: TABLE) -> None:
        self._db.begin()
        await self._db.delete(entry)
        await self._db.commit()
        return None  # pragma: no cover

    async def exists_by_fields(
        self,
        fields: dict[str, Any],
    ) -> TABLE | None:
        self._db.begin()
        conditions = [
            getattr(self._table, field_name) == field_value
            for field_name, field_value in fields.items()
        ]
        stmt: Select = sql_select(self._table).where(and_(*conditions))
        entry: Any = await self._get(stmt)
        if not entry:
            return None
        return entry
