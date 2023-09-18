from typing import Type

from app.crud.base import BaseRepository
from app.models import GcftSnapTrafficsource
from app.schemas import (
    GcftSnapTrafficsourceCreate,
    GcftSnapTrafficsourceRead,
    GcftSnapTrafficsourceUpdate,
)


class GcftSnapTrafficsourceRepository(
    BaseRepository[
        GcftSnapTrafficsourceCreate,
        GcftSnapTrafficsourceRead,
        GcftSnapTrafficsourceUpdate,
        GcftSnapTrafficsource,
    ]
):
    @property
    def _table(self) -> Type[GcftSnapTrafficsource]:  # type: ignore
        return GcftSnapTrafficsource
