from app.core.crud import BaseRepository
from app.entities.core_ipaddress_geocoord.model import IpaddressGeocoord
from app.entities.core_ipaddress_geocoord.schemas import (
    IpaddressGeocoordCreate,
    IpaddressGeocoordRead,
    IpaddressGeocoordUpdate,
)


class IpaddressGeocoordRepository(
    BaseRepository[
        IpaddressGeocoordCreate,
        IpaddressGeocoordRead,
        IpaddressGeocoordUpdate,
        IpaddressGeocoord,
    ]
):
    @property
    def _table(self) -> IpaddressGeocoord:
        return IpaddressGeocoord
