from typing import Type

from app.crud.base import BaseRepository
from app.models import Ipaddress
from app.schemas import IpaddressCreate, IpaddressRead, IpaddressUpdate


class IpaddressRepository(
    BaseRepository[IpaddressCreate, IpaddressRead, IpaddressUpdate, Ipaddress]
):
    @property
    def _table(self) -> Type[Ipaddress]:  # type: ignore
        return Ipaddress
