import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GcftSnapBrowserreportRepository
from app.models import GcftSnapBrowserreport

pytestmark = pytest.mark.asyncio


async def test_gcft_snap_browserreport_repo_table(db_session: AsyncSession) -> None:
    repo: GcftSnapBrowserreportRepository = GcftSnapBrowserreportRepository(
        session=db_session
    )
    assert repo._table is GcftSnapBrowserreport
