from app.core.crud import BaseRepository
from app.entities.gcft_snap_hotspot_click.model import GcftSnapHotspotclick
from app.entities.gcft_snap_hotspot_click.schemas import (
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
