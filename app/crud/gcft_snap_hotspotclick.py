from app.crud.base import BaseRepository
from app.models import GcftSnapHotspotclick
from app.schemas import (
    GcftSnapHotspotclickCreate,
    GcftSnapHotspotclickRead,
    GcftSnapHotspotclickUpdate,
)


class GcftSnapHotspotclickRepository(
    BaseRepository[
        GcftSnapHotspotclickCreate,
        GcftSnapHotspotclickRead,
        GcftSnapHotspotclickUpdate,
        GcftSnapHotspotclick,
    ]
):
    @property
    def _table(self) -> GcftSnapHotspotclick:
        return GcftSnapHotspotclick
