from typing import Type, Union

from app.core.security.permissions.access import RoleUser
from app.crud.base import BaseRepository
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate
from app.schemas.user import UserUpdateAsAdmin, UserUpdateAsManager


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> Type[User]:  # type: ignore
        return User

    async def add_privileges(
        self,
        entry: User,
        schema: UserUpdateAsAdmin | UserUpdateAsManager,
    ) -> User:
        user_scopes = entry.scopes
        input_scopes = schema.scopes
        # TODO: add validation to ensure that the scopes are valid
        if input_scopes:
            user_scopes.extend(input_scopes)
        entry.scopes = list(set(user_scopes))
        if isinstance(schema, UserUpdateAsAdmin):
            if schema.is_superuser is not None:
                entry.is_superuser = schema.is_superuser
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def remove_privileges(
        self,
        entry: User,
        schema: Union[UserUpdateAsAdmin, UserUpdateAsManager],
    ) -> User:
        user_scopes = entry.scopes
        remove_scopes = schema.scopes
        # TODO: add validation to ensure that the scopes are valid
        if remove_scopes:
            updated_scopes = [
                scope for scope in user_scopes if scope not in remove_scopes
            ]
        if RoleUser not in updated_scopes:
            updated_scopes.append(RoleUser)
        entry.scopes = list(set(updated_scopes))
        if isinstance(schema, UserUpdateAsAdmin):
            if schema.is_superuser is not None:
                entry.is_superuser = schema.is_superuser
        await self._db.commit()
        await self._db.refresh(entry)
        return entry
