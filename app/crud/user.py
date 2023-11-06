from typing import Type

from app.core.security.permissions.scope import AclPrivilege
from app.crud.base import BaseRepository
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.schemas.user import UserUpdatePrivileges


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> Type[User]:  # type: ignore
        return User

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
