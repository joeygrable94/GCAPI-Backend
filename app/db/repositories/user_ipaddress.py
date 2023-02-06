from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import UserIpCreate, UserIpRead, UserIpUpdate
from app.db.tables import UserIpAddress


class UserIpAddressRepository(
    BaseRepository[UserIpCreate, UserIpRead, UserIpUpdate, UserIpAddress]
):
    @property
    def _table(self) -> Type[UserIpAddress]:  # type: ignore
        return UserIpAddress
