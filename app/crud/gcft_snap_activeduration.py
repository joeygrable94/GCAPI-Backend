from typing import Type

from app.crud.base import BaseRepository
from app.models import GcftSnapActiveduration
from app.schemas import (
    GcftSnapActivedurationCreate,
    GcftSnapActivedurationRead,
    GcftSnapActivedurationUpdate,
)


class GcftSnapActivedurationRepository(
    BaseRepository[
        GcftSnapActivedurationCreate,
        GcftSnapActivedurationRead,
        GcftSnapActivedurationUpdate,
        GcftSnapActiveduration,
    ]
):
    @property
    def _table(self) -> Type[GcftSnapActiveduration]:  # type: ignore
        return GcftSnapActiveduration
