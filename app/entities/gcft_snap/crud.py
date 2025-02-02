from app.core.crud import BaseRepository
from app.entities.gcft_snap.model import GcftSnap
from app.entities.gcft_snap.schemas import GcftSnapCreate, GcftSnapRead, GcftSnapUpdate


class GcftSnapRepository(
    BaseRepository[GcftSnapCreate, GcftSnapRead, GcftSnapUpdate, GcftSnap]
):
    @property
    def _table(self) -> GcftSnap:
        return GcftSnap
