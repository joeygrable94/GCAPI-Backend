import abc
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import UUID4
from sqlalchemy import Select, select as sql_select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.utilities import get_uuid, paginate
from app.db.base import Base
from app.schemas.base import BaseSchema

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
    def _table(self) -> TABLE:
        pass  # pragma: no cover

    def gen_uuid(self) -> UUID4:
        return get_uuid()

    def _preprocess_create(self, values: Dict) -> Dict:  # pragma: no cover
        if "id" not in values:
            values["id"] = self.gen_uuid()
        return values

    async def _get(self, query: Any) -> Optional[TABLE]:
        results: Any = await self._db.execute(query)
        data: Any = results.first()
        if data is None:
            return None
        return data[0]

    async def _list(
        self, skip: int = 0, limit: int = settings.api.query_limit_rows_default
    ) -> Union[List[TABLE], List[None]]:
        query: Any = sql_select(self._table).offset(skip).limit(limit)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[TABLE] = result.scalars().all()  # pragma: no cover
        return data  # pragma: no cover

    def query_list(self) -> Select:
        stmt = sql_select(self._table)  # type: ignore
        return stmt

    async def list(
        self,
        page: int = 1,
    ) -> Optional[Union[List[TABLE], List[None]]]:
        self._db.begin()
        skip, limit = paginate(page)
        return await self._list(skip=skip, limit=limit)

    async def create(self, schema: Union[SCHEMA_CREATE, Any]) -> TABLE:
        self._db.begin()
        entry: Any = self._table(id=self.gen_uuid(), **schema.model_dump())  # type: ignore  # noqa: E501
        self._db.add(entry)
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def read_by(self, field_name: str, field_value: Any) -> Optional[TABLE]:
        self._db.begin()
        check_val: Any = getattr(self._table, field_name)
        query: Any = sql_select(self._table).where(check_val == field_value)  # type: ignore  # noqa: E501
        entry: Any = await self._get(query)
        if not entry:
            return None
        return entry

    async def read(self, entry_id: UUID4) -> Optional[TABLE]:
        self._db.begin()
        query: Any = sql_select(self._table).where(self._table.id == entry_id)  # type: ignore  # noqa: E501
        entry: Any = await self._get(query)
        if not entry:
            return None
        return entry

    async def update(
        self,
        entry: TABLE,
        schema: Union[SCHEMA_UPDATE, Any],
    ) -> Optional[TABLE]:
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

    async def exists_by_two(
        self,
        field_name_a: str,
        field_value_a: Any,
        field_name_b: str,
        field_value_b: Any,
    ) -> Optional[TABLE]:
        self._db.begin()
        check_val_a: Any = getattr(self._table, field_name_a)
        check_val_b: Any = getattr(self._table, field_name_b)
        query: Any = sql_select(self._table).where(  # type: ignore
            (check_val_a == field_value_a) & (check_val_b == field_value_b)
        )
        entry: Any = await self._get(query)
        if not entry:
            return None
        return entry
