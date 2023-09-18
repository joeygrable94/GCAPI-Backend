from typing import Type

from app.crud.base import BaseRepository
from app.models import GcftSnapBrowserreport
from app.schemas import (
    GcftSnapBrowserreportCreate,
    GcftSnapBrowserreportRead,
    GcftSnapBrowserreportUpdate,
)


class GcftSnapBrowserreportRepository(
    BaseRepository[
        GcftSnapBrowserreportCreate,
        GcftSnapBrowserreportRead,
        GcftSnapBrowserreportUpdate,
        GcftSnapBrowserreport,
    ]
):
    @property
    def _table(self) -> Type[GcftSnapBrowserreport]:  # type: ignore
        return GcftSnapBrowserreport
