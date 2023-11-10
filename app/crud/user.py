from typing import Sequence, Type

from sqlalchemy import Result, Select, select as sql_select

from app.core.security.permissions import AclPrivilege
from app.core.utilities import paginate
from app.crud.base import BaseRepository
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate, UserUpdatePrivileges


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> Type[User]:  # type: ignore
        return User

    async def get_list(
        self,
        page: int = 1,
    ) -> list[User] | list[None]:
        self._db.begin()
        skip, limit = paginate(page)
        query: Select = sql_select(self._table).offset(skip).limit(limit)
        result: Result = await self._db.execute(query)
        data: Sequence[User] = result.scalars().all()  # pragma: no cover
        data_list = list(data)
        return data_list

    async def add_privileges(
        self,
        entry: User,
        schema: UserUpdatePrivileges,
    ) -> list[AclPrivilege]:
        updated_scopes = entry.scopes
        if schema.scopes:
            updated_scopes.extend(schema.scopes)
        setattr(entry, "scopes", list(set(updated_scopes)))
        await self._db.commit()
        await self._db.refresh(entry, ["scopes"])
        return entry.scopes

    async def remove_privileges(
        self,
        entry: User,
        schema: UserUpdatePrivileges,
    ) -> list[AclPrivilege]:
        user_scopes = entry.scopes
        if schema.scopes:
            updated_scopes = [
                scope for scope in user_scopes if scope not in schema.scopes
            ]
        setattr(entry, "scopes", list(set(updated_scopes)))
        await self._db.commit()
        await self._db.refresh(entry, ["scopes"])
        return entry.scopes
