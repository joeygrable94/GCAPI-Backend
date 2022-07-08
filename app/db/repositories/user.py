from typing import Any, Dict, List, Optional, Type, Union

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.paginate import paginate
from app.db.repositories.base import BaseRepository
from app.db.schemas import UserCreate, UserRead, UserUpdate
from app.db.schemas.user import ID
from app.db.tables import User

from .base import PER_PAGE_MAX_COUNT  # type: ignore
from .base import sql_select


class UsersRepository(BaseRepository[UserCreate, UserUpdate, UserRead, User]):
    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session

    @property
    def _schema_read(self) -> Type[UserRead]:
        return UserRead

    @property
    def _table(self) -> Type[User]:
        return User

    async def _get(self, query: Any) -> Optional[User]:
        results: Any = await self._db.execute(query)
        user: Any = results.first()
        if user is None:
            return None
        return user[0]

    async def _list(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT
    ) -> Union[List[User], List[UserRead], List[Any]]:
        query: Any = sql_select(self._table).limit(limit).offset(skip)  # type: ignore
        result: Any = await self._db.execute(query)
        data: List[Any] = result.scalars().all()
        return data

    async def list(self, page: int = 1) -> Union[List[User], List[UserRead], List[Any]]:
        skip, limit = paginate(page)
        return await self._list(skip=skip, limit=limit)

    async def create(  # type: ignore
        self, schema: Dict[str, Any]  # type: ignore
    ) -> Optional[Union[User, UserRead]]:  # type: ignore
        user: Any = self._table(id=self.generate_uuid(), **schema)
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def read(  # type: ignore
        self, entry_id: ID
    ) -> Optional[Union[User, UserRead]]:  # type: ignore
        query: Any = sql_select(self._table).where(  # type: ignore
            self._table.id == entry_id
        )
        return await self._get(query)

    async def read_by_email(self, email: str) -> Optional[Union[User, UserRead]]:
        query: Any = sql_select(self._table).where(  # type: ignore
            func.lower(self._table.email) == func.lower(email)
        )
        return await self._get(query)

    async def update(  # type: ignore
        self, entry: Any, schema: Dict[str, Any]  # type: ignore
    ) -> Optional[Union[User, UserRead]]:  # type: ignore
        for key, value in schema.items():
            setattr(entry, key, value)
        self._db.add(entry)
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def delete(  # type: ignore
        self, entry: Any
    ) -> Optional[Union[User, UserRead]]:  # type: ignore
        await self._db.delete(entry)
        await self._db.commit()
        return entry
