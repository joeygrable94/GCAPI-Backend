from app.core.crud import BaseRepository
from app.entities.gcft_snap_active_duration.model import GcftSnapActiveduration
from app.entities.gcft_snap_active_duration.schemas import (
    GcftSnapActivedurationCreate,
    GcftSnapActivedurationRead,
    GcftSnapActivedurationUpdate,
)


class GcftSnapActivedurationRepository(
    BaseRepository[
        GcftSnapActivedurationCreate,
        GcftSnapActivedurationRead,
        GcftSnapActivedurationUpdate,
        GcftSnapActiveduration,
    ]
):
    @property
    def _table(self) -> GcftSnapActiveduration:
        return GcftSnapActiveduration
