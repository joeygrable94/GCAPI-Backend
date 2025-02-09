from app.core.crud import BaseRepository
from app.entities.core_geocoord.model import Geocoord
from app.entities.core_geocoord.schemas import (
    GeocoordCreate,
    GeocoordRead,
    GeocoordUpdate,
)


class GeocoordRepository(
    BaseRepository[GeocoordCreate, GeocoordRead, GeocoordUpdate, Geocoord]
):
    @property
    def _table(self) -> Geocoord:
        return Geocoord
