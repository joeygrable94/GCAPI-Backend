from app.crud.base import BaseRepository
from app.models import Gcft
from app.schemas import GcftCreate, GcftRead, GcftUpdate


class GcftRepository(BaseRepository[GcftCreate, GcftRead, GcftUpdate, Gcft]):
    @property
    def _table(self) -> Gcft:
        return Gcft
