from typing import Type

from app.crud.base import BaseRepository
from app.models import Sharpspring
from app.schemas import SharpspringCreate, SharpspringRead, SharpspringUpdate


class SharpspringRepository(
    BaseRepository[SharpspringCreate, SharpspringRead, SharpspringUpdate, Sharpspring]
):
    @property
    def _table(self) -> Type[Sharpspring]:  # type: ignore
        return Sharpspring
