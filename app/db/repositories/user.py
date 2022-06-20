from typing import Any, List, Type

from fastapi_users import schemas
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import AsyncSession, SQLAlchemyUserDatabase
from pydantic import UUID4

from app.core.logger import logger
from app.core.user_manager import UserManager
from app.db.errors import DoesNotExist
from app.db.repositories.base import BaseUserRepository
from app.db.schemas import UserCreate, UserRead, UserUpdate
from app.db.schemas import ClientRead
from app.db.tables import User

from .base import PER_PAGE_MAX_COUNT, sql_select


class UsersRepository(BaseUserRepository[UserCreate, UserUpdate, UserRead, User]):
    def __init__(self, session: AsyncSession, *args: Any, **kwargs: Any) -> None:
        self._db: AsyncSession = session
        self._user_db: SQLAlchemyUserDatabase = SQLAlchemyUserDatabase(session, User)
        self._user_manager: UserManager = UserManager(user_db=self._user_db)

    @property
    def _table(self) -> Type[User]:
        return User

    @property
    def _schema_create(self) -> Type[UserCreate]:
        return UserCreate

    @property
    def _schema_update(self) -> Type[UserUpdate]:
        return UserUpdate

    @property
    def _schema_read(self) -> Type[UserRead]:
        return UserRead

    async def _list(
        self, skip: int = 0, limit: int = PER_PAGE_MAX_COUNT
    ) -> List[UserRead]:
        query = sql_select(self._user_db.user_table).limit(limit).offset(skip)
        result = await self._user_db.session.execute(query)
        data = result.scalars().all()
        return list(data)

    async def list(self, page: int = 1) -> List[UserRead]:
        skip, limit = self.paginate(page)
        return await self._list(skip=skip, limit=limit)

    async def create(self, schema: UserCreate) -> UserRead:
        try:
            user = await self._user_manager.create(user_create=schema)
            return self._schema_read.from_orm(user)
        except UserAlreadyExists:
            logger.debug(f"User {schema.email} already exists")

    async def read(self, user_id: UUID4) -> UserRead:
        try:
            user = await self._user_manager.get(id=user_id)
            return self._schema_read.from_orm(user)
        except DoesNotExist:
            logger.debug(f"<User id={user_id}> does not exist")

    async def read_by_email(self, email: str) -> Any:
        try:
            user = await self._user_manager.get_by_email(user_email=email)
            return self._schema_read.from_orm(user)
        except DoesNotExist:
            logger.debug(f"<User email={email}> does not exist")

    async def update(self, user_id: UUID4, schema: UserUpdate) -> UserRead:
        try:
            user = await self._user_manager.get(id=user_id)
            user_updated = await self._user_manager.update(
                user_update=schema, user=user
            )
            return self._schema_read.from_orm(user_updated)
        except DoesNotExist:
            logger.debug(f"<User email={user_id}> does not exist")

    async def delete(self, user_id: UUID4) -> UserRead:
        try:
            user = await self._user_manager.get(id=user_id)
            await self._user_manager.delete(user=user)
            return self._schema_read.from_orm(user)
        except DoesNotExist:
            logger.debug(f"<User email={user_id}> does not exist")

    async def verify_password(self, password: str, check_user: schemas.UC) -> bool:
        try:
            is_valid = await self._user_manager.validate_password(
                password=password, user=check_user
            )
            if is_valid is None:
                return True
        except Exception:
            return False
