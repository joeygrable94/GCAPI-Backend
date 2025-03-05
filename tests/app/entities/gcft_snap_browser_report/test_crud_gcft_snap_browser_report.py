import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.gcft_snap_browser_report.crud import GcftSnapBrowserreportRepository
from app.entities.gcft_snap_browser_report.model import GcftSnapBrowserreport

pytestmark = pytest.mark.anyio


async def test_gcft_snap_browserreport_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapBrowserreportRepository = GcftSnapBrowserreportRepository(
        session=db_session
    )
    assert repo._table is GcftSnapBrowserreport
