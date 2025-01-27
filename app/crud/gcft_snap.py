from app.crud.base import BaseRepository
from app.models import GcftSnap
from app.schemas import GcftSnapCreate, GcftSnapRead, GcftSnapUpdate


class GcftSnapRepository(
    BaseRepository[GcftSnapCreate, GcftSnapRead, GcftSnapUpdate, GcftSnap]
):
    @property
    def _table(self) -> GcftSnap:
        return GcftSnap
