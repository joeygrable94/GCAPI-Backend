from app.core.crud import BaseRepository
from app.entities.gcft.model import Gcft
from app.entities.gcft.schemas import GcftCreate, GcftRead, GcftUpdate


class GcftRepository(BaseRepository[GcftCreate, GcftRead, GcftUpdate, Gcft]):
    @property
    def _table(self) -> Gcft:
        return Gcft
