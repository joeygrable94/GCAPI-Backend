import abc
from typing import Dict, Generic, List, Mapping, Type, TypeVar
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import Table
from sqlalchemy import select as sql_select
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.errors import DoesNotExist
from app.db.schemas.base import BaseSchema

SCHEMA_CREATE = TypeVar("SCHEMA_CREATE", bound=BaseSchema)
SCHEMA_UPDATE = TypeVar("SCHEMA_UPDATE", bound=BaseSchema)
SCHEMA_READ = TypeVar("SCHEMA_READ", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Table)


class BaseRepository(
    Generic[SCHEMA_CREATE, SCHEMA_UPDATE, SCHEMA_READ, TABLE], metaclass=abc.ABCMeta
):
    def __init__(self, session: AsyncSession, *args, **kwargs) -> None:
        self._db: AsyncSession = session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        pass

    @property
    @abc.abstractmethod
    def _schema_create(self) -> Type[SCHEMA_CREATE]:
        pass

    @property
    @abc.abstractmethod
    def _schema_update(self) -> Type[SCHEMA_UPDATE]:
        pass

    @property
    @abc.abstractmethod
    def _schema_read(self) -> Type[SCHEMA_READ]:
        pass

    @staticmethod
    def generate_uuid() -> UUID4:
        return uuid4()

    @staticmethod
    def paginate(page: int = 1) -> tuple[int, int]:
        """
        in      pg      skip    limit
        -1      1       000     100       0-100
         0      1       000     100       0-100
         1      1       000     100       0-100
         2      2       100     100     100-200
         3      3       200     100     200-300
         4      4       300     100     300-400
        """
        limit = 100
        page = 1 if page < 1 else page
        skip = 0 if page == 1 else (page - 1) * limit
        return skip, limit

    def _preprocess_create(self, values: Dict) -> Dict:
        if "id" not in values:
            values["id"] = self.generate_uuid()
        return values

    async def _list(self, skip: int = 0, limit: int = 100) -> List[Mapping]:
        query = sql_select(self._table).offset(skip).limit(limit)
        result = await self._db.execute(query)
        return result.scalars().all()

    async def list(self, page: int = 1) -> List[Mapping]:
        skip, limit = self.paginate(page)
        return await self._list(skip=skip, limit=limit)

    async def create(self, schema: SCHEMA_CREATE) -> SCHEMA_READ:
        entry = self._table(id=self.generate_uuid(), **schema.dict())
        self._db.add(entry)
        await self._db.commit()
        return self._schema_read.from_orm(entry)

    async def read(self, entry_id: UUID4) -> SCHEMA_READ:
        query = sql_select(self._table).where(self._table.id == entry_id)
        result = await self._db.execute(query)
        entry = result.scalars().first()
        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<id:{entry_id}> does not exist")
        return self._schema_read.from_orm(entry)

    async def update(self, entry_id: UUID4, schema: SCHEMA_UPDATE) -> SCHEMA_READ:
        entry = await self._db.get(self._table, entry_id)
        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<id:{entry_id}> does not exist")
        query = (
            sql_update(self._table)
            .where(entry.id == entry_id)
            .values(**schema.dict())
            .execution_options(synchronize_session="fetch")
        )
        await self._db.execute(query)
        await self._db.commit()
        await self._db.refresh(entry)
        return self._schema_read.from_orm(entry)

    async def delete(self, entry_id: UUID4) -> SCHEMA_READ:
        entry = await self._db.get(self._table, entry_id)
        if not entry:
            raise DoesNotExist(f"{self._table.__name__}<id:{entry_id}> does not exist")
        await self._db.delete(entry)
        await self._db.commit()
        return self._schema_read.from_orm(entry)
