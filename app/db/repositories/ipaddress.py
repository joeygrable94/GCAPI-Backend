from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import IpAddressCreate, IpAddressRead, IpAddressUpdate
from app.db.tables import IpAddress


class IpAddressRepository(
    BaseRepository[IpAddressCreate, IpAddressRead, IpAddressUpdate, IpAddress]
):
    @property
    def _table(self) -> Type[IpAddress]:  # type: ignore
        return IpAddress
