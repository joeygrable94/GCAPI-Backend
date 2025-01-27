from app.crud.base import BaseRepository
from app.models import GcftSnapView
from app.schemas import GcftSnapViewCreate, GcftSnapViewRead, GcftSnapViewUpdate


class GcftSnapViewRepository(
    BaseRepository[
        GcftSnapViewCreate, GcftSnapViewRead, GcftSnapViewUpdate, GcftSnapView
    ]
):
    @property
    def _table(self) -> GcftSnapView:
        return GcftSnapView
