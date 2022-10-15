from typing import Any, Optional, Type

from sqlalchemy import func, select

from app.api.exceptions import UserAlreadyExists, UserNotExists
from app.db.repositories.base import BaseRepository
from app.db.schemas import UserCreate, UserRead, UserUpdate
from app.db.tables import User
from app.security import password_helper


class UsersRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _schema_read(self) -> Type[UserRead]:  # type: ignore
        return UserRead

    @property
    def _table(self) -> Type[User]:  # type: ignore
        return User

    async def create(self, schema: UserCreate) -> User:
        await password_helper.validate_password(schema.password)
        found: Optional[User] = await self.read_by_email(schema.email)
        if found is not None:
            raise UserAlreadyExists()
        user_dict = schema.dict()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = password_helper.hash(password)
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
        for f, v in schema.dict(exclude_unset=True).items():
            if f == "email" and v != entry.email:
                try:  # pragma: no cover
                    found: Optional[User] = await self.read_by_email(v)
                    if found is None:
                        raise UserNotExists()
                    raise UserAlreadyExists()
                except UserNotExists:  # pragma: no cover
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
