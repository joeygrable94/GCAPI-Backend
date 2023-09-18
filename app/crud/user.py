from typing import Type

from app.crud.base import BaseRepository
from app.models import User
from app.schemas import UserCreate, UserRead, UserUpdate


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate, User]):
    @property
    def _table(self) -> Type[User]:  # type: ignore
        return User
