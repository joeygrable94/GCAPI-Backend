from typing import Any, List, Optional, Type

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select

from app.api.exceptions import ApiAuthException, UserAlreadyExists, UserNotExists
from app.core.utilities import password_helper
from app.db.repositories.base import BaseRepository
from app.db.schemas import UserCreate, UserRead, UserUpdate, UserUpdateAuthPermissions
from app.db.tables import User


class UsersRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> Type[User]:  # type: ignore
        return User

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        try:
            user: Optional[User] = await self.read_by_email(credentials.username)
        except UserNotExists:  # pragma: no cover
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            password_helper.hash(credentials.password)
        if not user:
            return None
        verified, updated_password_hash = password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None  # pragma: no cover
        if updated_password_hash is not None:
            await self.update(  # pragma: no cover
                entry=user, schema=UserUpdate(hashed_password=updated_password_hash)
            )
        return user

    async def create(self, schema: UserCreate) -> User:
        await password_helper.validate_password(schema.password)
        found: Optional[User] = await self.read_by_email(schema.email)
        if found is not None:
            raise UserAlreadyExists()
        user_dict = schema.dict()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = password_helper.hash(password)
        # START acl_principals
        user_dict["principals"] = []
        # ADMINS
        if user_dict["is_superuser"]:
            user_dict["principals"].append("role:admin")
        # ALL USERS
        user_dict["principals"].append("role:user")
        user_dict["principals"].append("user:%s" % user_dict["email"])
        # END acl_principals
        entry: Any = self._table(id=self.gen_uuid(), **user_dict)
        self._db.add(entry)
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def read_by_email(self, email: str) -> Optional[User]:
        query: Any = select(self._table).where(  # type: ignore
            func.lower(self._table.email) == func.lower(email)
        )
        return await self._get(query)

    async def update(self, entry: User, schema: UserUpdate) -> User:  # type: ignore
        valid_dict = {}
        for f, v in schema.dict(exclude_unset=True, exclude_none=True).items():
            if f == "email" and v != entry.email:  # pragma: no cover
                try:
                    found: Optional[User] = await self.read_by_email(v)
                    if found is None:
                        raise UserNotExists()
                    raise UserAlreadyExists()
                except UserNotExists:
                    valid_dict["email"] = v
                    valid_dict["is_verified"] = False
            elif f == "password":
                await password_helper.validate_password(v)
                valid_dict["hashed_password"] = password_helper.hash(v)
            else:
                valid_dict[f] = v
        for k, d in valid_dict.items():
            setattr(entry, k, d)
        await self._db.commit()
        await self._db.refresh(entry)
        return entry

    async def updatePermissions(
        self, entry: User, schema: UserUpdateAuthPermissions, method: str
    ) -> User:  # type: ignore
        user_permissions: List[str] = []
        for f, v in schema.dict(exclude_unset=True, exclude_none=True).items():
            if f == "email":
                if v == entry.email:
                    try:
                        found: Optional[User] = await self.read_by_email(v)
                        if not found:
                            raise UserNotExists()  # pragma: no cover
                    except UserNotExists:  # pragma: no cover
                        raise ApiAuthException(
                            "cannot update the permissions of the requested user"
                        )
                else:
                    raise ApiAuthException("email must match the user to update")
            if f == "principals":
                if method in ["add", "append", "extend"]:
                    user_permissions = list(entry.principals)
                    user_permissions.extend(p for p in v if p not in user_permissions)
                elif method in ["remove", "delete", "trim"]:
                    user_permissions = [i for i in entry.principals if i not in v]
        valid_dict = {"principals": user_permissions}
        for k, d in valid_dict.items():
            setattr(entry, k, d)
        await self._db.commit()
        await self._db.refresh(entry)
        return entry
