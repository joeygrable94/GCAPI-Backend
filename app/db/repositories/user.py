from typing import Any, List, Optional, Type, Union

from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user_manager import UserManager
from app.core.user_manager.sqlalchemy_adapter import SQLAlchemyUserDatabase
from app.db.repositories.base import BaseRepository
from app.db.schemas.user import UserCreate, UserRead, UserUpdate
from app.db.tables import User

from .base import PER_PAGE_MAX_COUNT, sql_select


class UsersRepository(BaseRepository[UserCreate, UserUpdate, UserRead, User]):
    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session
        self._user_db: SQLAlchemyUserDatabase = SQLAlchemyUserDatabase(session, User)
        self._user_manager: UserManager = UserManager(user_db=self._user_db)

    @property
    def _table(self) -> Type[User]:
        return User

    @property
    def _schema_read(self) -> Type[UserRead]:
        return UserRead

    async def _list(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT
    ) -> Union[List[UserRead], List]:  # type: ignore
        query: Any = (
            sql_select(self._user_db.user_table)  # type: ignore
            .limit(limit)
            .offset(skip)
        )
        result: Any = await self._user_db.session.execute(query)
        data: Any = result.scalars().all()
        return list(data)

    async def list(self, page: int = 1) -> Union[List[UserRead], List]:  # type: ignore
        skip, limit = self.paginate(page)
        return await self._list(skip=skip, limit=limit)

    async def create(self, schema: UserCreate) -> Optional[UserRead]:  # type: ignore
        user: Any = await self._user_manager.create(user_create=schema)
        return self._schema_read.from_orm(user)  # type: ignore

    async def read(self, user_id: UUID4) -> UserRead:  # type: ignore
        user: Any = await self._user_manager.get(id=user_id)
        return self._schema_read.from_orm(user)  # type: ignore

    async def read_by_email(self, email: str) -> UserRead:  # type: ignore
        user: Any = await self._user_manager.get_by_email(user_email=email)
        return self._schema_read.from_orm(user)  # type: ignore

    async def update(  # type: ignore
        self, user_id: UUID4, schema: UserUpdate
    ) -> Optional[UserRead]:
        user: Any = await self._user_manager.get(id=user_id)
        user_updated: Any = await self._user_manager.update(
            user_update=schema, user=user
        )
        return self._schema_read.from_orm(user_updated)  # type: ignore

    async def delete(self, user_id: UUID4) -> Optional[UserRead]:  # type: ignore
        user: Any = await self._user_manager.get(id=user_id)
        await self._user_manager.delete(user=user)
        return self._schema_read.from_orm(user)  # type: ignore
