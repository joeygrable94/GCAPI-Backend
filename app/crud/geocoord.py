from app.crud.base import BaseRepository
from app.models import Geocoord
from app.schemas import GeocoordCreate, GeocoordRead, GeocoordUpdate


class GeocoordRepository(
    BaseRepository[GeocoordCreate, GeocoordRead, GeocoordUpdate, Geocoord]
):
    @property
    def _table(self) -> Geocoord:
        return Geocoord
