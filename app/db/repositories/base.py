import abc
from typing import Any, Dict, Generic, List, Type, TypeVar

from pydantic import UUID4
from sqlalchemy import Table
from sqlalchemy import select as sql_select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.base import BaseSchema
from app.db.utilities import _get_uuid

SCHEMA_CREATE = TypeVar("SCHEMA_CREATE", bound=BaseSchema)
SCHEMA_READ = TypeVar("SCHEMA_READ", bound=BaseSchema)
SCHEMA_UPDATE = TypeVar("SCHEMA_UPDATE", bound=BaseSchema)
TABLE = TypeVar("TABLE", bound=Table)
PER_PAGE_MAX_COUNT: int = 100


class BaseRepository(
    Generic[SCHEMA_CREATE, SCHEMA_READ, SCHEMA_UPDATE, TABLE], metaclass=abc.ABCMeta
):
    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session

    @property
    @abc.abstractmethod
    def _schema_create(self) -> Type[SCHEMA_CREATE]:
        pass

    @property
    @abc.abstractmethod
    def _schema_read(self) -> Type[SCHEMA_READ]:
        pass

    @property
    @abc.abstractmethod
    def _schema_update(self) -> Type[SCHEMA_UPDATE]:
        pass

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        pass

    @staticmethod
    def generate_uuid() -> UUID4:
        return _get_uuid()

    @staticmethod
    def paginate(page: int = 1, limit: int = PER_PAGE_MAX_COUNT) -> tuple[int, int]:
        """A simple pagination utility.

        Args:
            page (int, optional): the page to fetch rows for. Defaults to 1.
            ppmax (int, optional): the Per Page Maximum or limit on how many items to return. Defaults to 100.

        Returns:
            tuple[int, int]: tuple contains a skip and limit, both integers.
            - Skip is the starting point at which the database should fetch items.
            - Limit is the total amount of items to return from the database.

        Example Input & Output:
            input   page    skip    limit
             -1     0       0       100       0-100
              0     1       0       100       0-100
              1     1       0       100       0-100
              2     2       100     100     100-200
              3     3       200     100     200-300
              4     4       300     100     300-400
        """
        page = 1 if page < 1 else page
        skip = 0 if page == 1 else (page - 1) * limit
        return skip, limit

    def _preprocess_create(self, values: Dict) -> Dict:
        if "id" not in values:
            values["id"] = self.generate_uuid()
        return values

    async def _list(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT
    ) -> List[SCHEMA_READ]:
        query = sql_select(self._table).offset(skip).limit(limit)
        result = await self._db.execute(query)
        data = result.scalars().all()
        return list(data)

    async def list(self, page: int = 1) -> List[SCHEMA_READ]:
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
            return None
        return self._schema_read.from_orm(entry)

    async def update(self, entry_id: UUID4, schema: SCHEMA_UPDATE) -> SCHEMA_READ:
        query = sql_select(self._table).where(self._table.id == entry_id)
        result = await self._db.execute(query)
        entry = result.scalars().first()
        if not entry:
            return None
        for k, v in schema.dict(exclude_unset=True).items():
            setattr(entry, k, v)
        # await self._db.execute(query) ? double db exec (1st 6 lines above)
        await self._db.commit()
        await self._db.refresh(entry)
        return self._schema_read.from_orm(entry)

    async def delete(self, entry_id: UUID4) -> SCHEMA_READ:
        entry = await self._db.get(self._table, entry_id)
        if not entry:
            return None
        await self._db.delete(entry)
        await self._db.commit()
        return self._schema_read.from_orm(entry)


class BaseUserRepository(
    Generic[SCHEMA_CREATE, SCHEMA_READ, SCHEMA_UPDATE, TABLE], metaclass=abc.ABCMeta
):
    """This is a port for the Base Repository and the FastAPI_Users dependency.

    Args:
        Generic (class[C, R, U, T]): generic repository constructor;
        - takes in schemas Create, Read, Update
        - takes in Table ORM Mapper
        metaclass (class): optional db metaclass. Defaults to abc.ABCMeta.
    """

    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session

    @property
    @abc.abstractmethod
    def _schema_create(self) -> Type[SCHEMA_CREATE]:
        pass

    @property
    @abc.abstractmethod
    def _schema_read(self) -> Type[SCHEMA_READ]:
        pass

    @property
    @abc.abstractmethod
    def _schema_update(self) -> Type[SCHEMA_UPDATE]:
        pass

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        pass

    @staticmethod
    def paginate(page: int = 1, limit: int = PER_PAGE_MAX_COUNT) -> tuple[int, int]:
        page = 1 if page < 1 else page
        skip = 0 if page == 1 else (page - 1) * limit
        return skip, limit

    @abc.abstractmethod
    async def _list(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT
    ) -> List[SCHEMA_READ]:
        pass

    @abc.abstractmethod
    async def list(self, page: int = 1) -> List[SCHEMA_READ]:
        pass

    @abc.abstractmethod
    async def create(self, schema: SCHEMA_CREATE) -> SCHEMA_READ:
        pass

    @abc.abstractmethod
    async def read(self, user_id: UUID4) -> SCHEMA_READ:
        pass

    @abc.abstractmethod
    async def update(self, user_id: UUID4, schema: SCHEMA_UPDATE) -> SCHEMA_READ:
        pass

    @abc.abstractmethod
    async def delete(self, user_id: UUID4) -> SCHEMA_READ:
        pass
