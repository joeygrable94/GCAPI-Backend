from app.core.crud import BaseRepository
from app.entities.gcft_snap_traffic_source.model import GcftSnapTrafficsource
from app.entities.gcft_snap_traffic_source.schemas import (
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
