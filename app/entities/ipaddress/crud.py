from app.core.crud import BaseRepository
from app.entities.ipaddress.model import Ipaddress
from app.entities.ipaddress.schemas import (
    IpaddressCreate,
    IpaddressRead,
    IpaddressUpdate,
)


class IpaddressRepository(
    BaseRepository[IpaddressCreate, IpaddressRead, IpaddressUpdate, Ipaddress]
):
    @property
    def _table(self) -> Ipaddress:
        return Ipaddress
