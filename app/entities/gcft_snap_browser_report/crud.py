from app.core.crud import BaseRepository
from app.entities.gcft_snap_browser_report.model import GcftSnapBrowserreport
from app.entities.gcft_snap_browser_report.schemas import (
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
    def _table(self) -> GcftSnapBrowserreport:
        return GcftSnapBrowserreport
