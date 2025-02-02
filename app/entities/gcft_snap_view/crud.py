from app.core.crud import BaseRepository
from app.entities.gcft_snap_view.model import GcftSnapView
from app.entities.gcft_snap_view.schemas import (
    GcftSnapViewCreate,
    GcftSnapViewRead,
    GcftSnapViewUpdate,
)


class GcftSnapViewRepository(
    BaseRepository[
        GcftSnapViewCreate, GcftSnapViewRead, GcftSnapViewUpdate, GcftSnapView
    ]
):
    @property
    def _table(self) -> GcftSnapView:
        return GcftSnapView
