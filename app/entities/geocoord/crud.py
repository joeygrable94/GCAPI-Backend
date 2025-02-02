from app.core.crud import BaseRepository
from app.entities.geocoord.model import Geocoord
from app.entities.geocoord.schemas import GeocoordCreate, GeocoordRead, GeocoordUpdate


class GeocoordRepository(
    BaseRepository[GeocoordCreate, GeocoordRead, GeocoordUpdate, Geocoord]
):
    @property
    def _table(self) -> Geocoord:
        return Geocoord
