from app.crud.base import BaseRepository
from app.models import GcftSnapTrafficsource
from app.schemas import (
    GcftSnapTrafficsourceCreate,
    GcftSnapTrafficsourceRead,
    GcftSnapTrafficsourceUpdate,
)


class GcftSnapTrafficsourceRepository(
    BaseRepository[
        GcftSnapTrafficsourceCreate,
        GcftSnapTrafficsourceRead,
        GcftSnapTrafficsourceUpdate,
        GcftSnapTrafficsource,
    ]
):
    @property
    def _table(self) -> GcftSnapTrafficsource:
        return GcftSnapTrafficsource
