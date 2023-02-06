from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import UserClientCreate, UserClientRead, UserClientUpdate
from app.db.tables import UserClient


class UserClientRepository(
    BaseRepository[UserClientCreate, UserClientRead, UserClientUpdate, UserClient]
):
    @property
    def _table(self) -> Type[UserClient]:  # type: ignore
        return UserClient
